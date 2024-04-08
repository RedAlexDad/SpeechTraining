import "./Hearing.sass";
import {useEffect, useState} from "react";
import axios from "axios";
import Button from "@mui/material/Button";
import {useToken} from "../../Hooks/useToken.ts";

interface Accuracy {
    wer: number | null;
    cer: number | null;
    mer: number | null;
    wil: number | null;
    iwer: number | null;
}

export default function HearingPage() {
    const {access_token} = useToken();
    const [textToSynthesize, setTextToSynthesize] = useState<string>('');
    const [isRecording, setIsRecording] = useState<boolean>(false);
    const [isSynthesized, setIsSynthesized] = useState<boolean>(false); // Добавляем состояние для отслеживания успешного синтеза
    const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
    const [collectionWords, setCollectionWords] = useState<string[]>([]); // Состояние для хранения слов из текущей коллекции
    const [showCollectionWords, setShowCollectionWords] = useState<boolean>(false); // Состояние для отображения слов из коллекции
    const [userInput, setUserInput] = useState<string>(''); // Состояние для введенного пользователем текста
    const [isInputClosed, setIsInputClosed] = useState<boolean>(false); // Состояние для отслеживания закрытия input

    const [currentCollectionIndex, setCurrentCollectionIndex] = useState<number>(0);
    const sentencesCollections: string[][] = [
        ["привет"],
        ["как дела?"],
        ["тестирование"],
        ["другой пример слова"],
        ["другой пример слова 2"],
        // Добавьте больше коллекций по вашему усмотрению
    ];

    const startRecording = () => {
        setIsRecording(true);
        const currentCollection = sentencesCollections[currentCollectionIndex];

        axios.post('http://127.0.0.1:8000/api/create_speech_synthesis/', {text: currentCollection}, {
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                authorization: access_token,
            },
            responseType: 'blob'
        })
            .then(response => {
                const data = response.data;
                const blob = new Blob([data], {type: 'audio/mpeg'}); // Создаем Blob из полученных данных
                const audio = new Audio(URL.createObjectURL(blob)); // Создаем аудио из Blob
                audio.play();

                setCollectionWords(currentCollection); // Сохраняем слова из текущей коллекции в состоянии
                setAudioBlob(new Blob([data])); // Сохраняем Blob в переменную
                setIsSynthesized(true); // Устанавливаем флаг успешного синтеза
                setIsRecording(false); // Устанавливаем флаг окончания синтеза речи
            })
            .catch(error => {
                console.error('Ошибка при выполнении запроса на синтез речи:', error);
                setIsSynthesized(false);
                setIsRecording(false); // Устанавливаем флаг окончания синтеза речи
            });
    };

    const listenSynthesized = () => {
        if (isSynthesized && audioBlob) {
            const audio = new Audio();
            audio.src = URL.createObjectURL(audioBlob); // Создаем объект URL с использованием сохраненного Blob
            audio.play();
        }
    };

    const switchCollection = () => {
        setIsSynthesized(false);
        setShowCollectionWords(false);
        setCurrentCollectionIndex((prevIndex) => (prevIndex + 1) % sentencesCollections.length);
    };

    // Функция для проверки совпадения слов и подсветки неправильных слов
    const checkMatchingWords = () => {
        return collectionWords.map((word, index) => (
            <span key={index} className={word === userInput ? 'correct' : 'error'}>
                {word}
            </span>
        ));
    };

    // Функция для обработки проверки своего слуха
    const handleCheckMyHearing = () => {
        setIsSynthesized(false);
        setShowCollectionWords(true); // После нажатия на кнопку "Проверить свой слух" показываем слова из коллекции
        setIsInputClosed(true); // Закрываем input
    };

    useEffect(() => {
        // При изменении коллекции обновляем текст для синтеза
        setTextToSynthesize(sentencesCollections[currentCollectionIndex][0]);
        setIsSynthesized(false); // Сбрасываем флаг успешного синтеза при изменении коллекции
        setUserInput(''); // Сбрасываем введенный пользователем текст при изменении коллекции
        setIsInputClosed(false); // Открываем input
    }, [currentCollectionIndex]);

    return (
        <>
            <div className="hearing-page-wrapper">
                <h1 style={{fontSize: '1.5em', textAlign: 'center'}}>Проверить слух</h1>
                {/* Показываем слова из коллекции только после нажатия на кнопку "Проверить свой слух" */}
                {showCollectionWords && (
                    <div className="text-wrapper">
                        <p>{checkMatchingWords()}</p>
                    </div>
                )}
                <div className="text-input-wrapper">
                    <input
                        type="text"
                        value={userInput}
                        onChange={(e) => setUserInput(e.target.value)}
                        disabled={isInputClosed} // Делаем input неактивным, если isInputClosed = true
                    />
                    {/* Добавляем кнопку для проверки своего слуха */}
                    <Button
                        variant="outlined"
                        sx={{color: 'black', borderColor: 'white'}}
                        onClick={handleCheckMyHearing} disabled={!isSynthesized}
                    >
                        Проверить свой слух
                    </Button>
                </div>
            </div>
            <div className="record-button-wrapper">
                {!isSynthesized && (
                    <Button
                        variant="outlined"
                        sx={{color: 'white', borderColor: 'white'}}
                        onClick={startRecording} disabled={isRecording}
                    >
                        {isRecording ? 'Идет синтез речи...' : 'Синтезировать речь'}
                    </Button>
                )}
                {/*Делаем кнопку послушать активной только после успешного синтеза*/}
                {isSynthesized && (
                    <Button
                        variant="outlined"
                        sx={{color: 'white', borderColor: 'white'}}
                        onClick={listenSynthesized} disabled={!isSynthesized}
                    >
                        Послушать еще раз
                    </Button>
                )}
                <Button
                    variant="outlined"
                    sx={{color: 'white', borderColor: 'white'}}
                    onClick={switchCollection}
                >
                    Переключить коллекцию случайных словарей
                </Button>
            </div>
        </>
    );
};
