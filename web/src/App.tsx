import React, {useState, useEffect} from 'react';
import axios from 'axios';

const App: React.FC = () => {
    const [transcription, setTranscription] = useState<string>('');
    const [accuracy, setAccuracy] = useState<string>('');
    const [isRecording, setIsRecording] = useState<boolean>(false);

    const [currentCollectionIndex, setCurrentCollectionIndex] = useState<number>(0);
    const sentencesCollections: string[][] = [
        ["Привет"],
        ["Как дела?"],
        ["Другой пример слова"],
        ["Другой пример слова 2"],
        // Добавьте больше коллекций по вашему усмотрению
    ];

    const startRecording = () => {
        // Здесь вы можете добавить код для начала записи
        setIsRecording(true);
        const currentCollection = sentencesCollections[currentCollectionIndex];

        axios.post('http://127.0.0.1:8000/api/transcribe/', {sentences: currentCollection})
            .then(response => {
                const data = response.data;
                setTranscription(data.text);
                setAccuracy(data.error_percentage);
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
            <span key={index} style={{ color: char === splitTranscription[index] ? 'red' : 'green' }}>
                {char}
            </span>
        ));

        return highlightedText;
    };

    useEffect(() => {
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <p>Прочитайте этот текст: </p>
                {sentencesCollections[currentCollectionIndex].map((sentence: string, index: number) => (
                    <p key={index}>
                        {renderHighlightedText(sentence, transcription)}
                    </p>
                ))}
                <br/>
                <p>Распознанный текст: {transcription}</p>
                <p>Процент ошибок произношения: {accuracy}%</p>
                <button onClick={startRecording} disabled={isRecording}>
                    {isRecording ? 'Идет запись...' : 'Начать запись'}
                </button>
                <button onClick={switchCollection}>
                    Переключить коллекцию
                </button>
            </header>
        </div>
    );
};

export default App;
