import "./Speech.sass"
import {Link} from "react-router-dom";
import {motion} from 'framer-motion';
import {useEffect, useState} from "react";
import axios from "axios";
import Button from "@mui/material/Button";
import {useToken} from "../../Hooks/useToken.ts";
import {DOMEN} from "../../Consts.ts";

interface Accuracy {
    wer: number | null;
    cer: number | null;
    mer: number | null;
    wil: number | null;
    iwer: number | null;
}

export default function SpeechPage() {
    const {access_token} = useToken()
    const [transcription, setTranscription] = useState<string>('');
    const [accuracy, setAccuracy] = useState<Accuracy>({wer: null, cer: null, mer: null, wil: null, iwer: null});
    const [isRecording, setIsRecording] = useState<boolean>(false);

    const [currentCollectionIndex, setCurrentCollectionIndex] = useState<number>(0);
    const sentencesCollections: string[][] = [
        ["привет"],
        ["как дела?"],
        ["тестирование"],
        ["другой пример слова"],
        ["другой имер слова 2"],
        // Добавьте больше коллекций по вашему усмотрению
    ];

    const startRecording = () => {
        // Здесь вы можете добавить код для начала записи
        setIsRecording(true);
        const currentCollection = sentencesCollections[currentCollectionIndex];

        axios.post(`${DOMEN}transcribe/`, {
            sentences: currentCollection,
        }, {
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                authorization: access_token,
            },
        })
            .then(response => {
                const data = response.data;
                console.log(data);
                setTranscription(data.transcription_word);
                setAccuracy({
                    wer: data.wer,
                    cer: data.cer,
                    mer: data.mer,
                    wil: data.wil,
                    iwer: data.iwer
                });
                // console.log(data);
            })
            .catch(error => {
                console.error('Ошибка при выполнении запроса:', error);
                // Дополнительная обработка ошибок, если необходимо
            })
            .finally(() => {
                // Здесь вы можете добавить код для завершения записи
                setIsRecording(false);
            });
    };

    const switchCollection = () => {
        setCurrentCollectionIndex((prevIndex) => (prevIndex + 1) % sentencesCollections.length);
    };

    const renderHighlightedText = (sentence: string, transcription: string) => {
        const splitSentence = sentence.split('');
        const splitTranscription = transcription.split('');
        const highlightedText = splitSentence.map((char, index) => (
            <span key={index} className={char === splitTranscription[index] ? 'correct' : 'error'}>
            {char}
        </span>
        ));

        return highlightedText;
    };

    useEffect(() => {
    }, []);

    return (
        <>
            <div className="speech-page-wrapper">
                <h1 style={{fontSize: '1.5em', textAlign: 'center'}}>Прочитайте текст</h1>
                <div className="text-wrapper">
                    {sentencesCollections[currentCollectionIndex].map((sentence: string, index: number) => (
                        <p key={index}>
                            {renderHighlightedText(sentence, transcription)}
                        </p>
                    ))}
                </div>
                {transcription &&
                    <div>
                        <h1 style={{fontSize: '1.5em', textAlign: 'center'}}>Распознанный текст</h1>
                        <div className="text-wrapper">
                            <p>{transcription}</p>
                        </div>
                    </div>
                }
                <div className="accuracy-wrapper">
                    {accuracy.wer !== null && accuracy.cer !== null && accuracy.mer !== null && accuracy.wil !== null && accuracy.iwer !== null && (
                        <>
                            <p style={{fontSize: '1.2em'}}>Метрика WER: {accuracy.wer.toFixed(3)}</p>
                            <p style={{fontSize: '1.2em'}}>Метрика CER: {accuracy.cer.toFixed(3)}</p>
                            <p style={{fontSize: '1.2em'}}>Метрика MER: {accuracy.mer.toFixed(3)}</p>
                            <p style={{fontSize: '1.2em'}}>Метрика WIL: {accuracy.wil.toFixed(3)}</p>
                            <p style={{fontSize: '1.2em'}}>Метрика IWER: {accuracy.iwer.toFixed(3)}</p>
                        </>
                    )}
                </div>
            </div>
            <div className="record-button-wrapper">
                <Button
                    variant="outlined"
                    sx={{color: 'white', borderColor: 'white'}}
                    onClick={startRecording} disabled={isRecording}
                >
                    {isRecording ? 'Идет запись...' : 'Начать запись'}
                </Button>
                <Button
                    variant="outlined"
                    sx={{color: 'white', borderColor: 'white'}}
                    onClick={switchCollection}
                >
                    Переключить коллекцию
                </Button>
            </div>
        </>
    );
}