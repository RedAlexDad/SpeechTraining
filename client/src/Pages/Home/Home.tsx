import "./Home.sass"
import {Link} from "react-router-dom";
import { motion } from 'framer-motion';
import {useEffect, useState} from "react";
import axios from "axios";

export default function HomePage() {
	const [transcription, setTranscription] = useState<string>('');
	const [accuracy, setAccuracy] = useState({wer: null, cer: null, mer: null, wil: null});
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

		axios.post('http://127.0.0.1:8000/api/transcribe/', {sentences: currentCollection})
			.then(response => {
				const data = response.data;
				setTranscription(data.text);
				setAccuracy({wer: data.wer, cer: data.cer, mer: data.mer, wil: data.wil});
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
		<div className="home-page-wrapper">
			<div className="voice-animation-wrapper">
				{/*<motion.div*/}
				{/*	className="voice-icon"*/}
				{/*	initial={{ scale: 1 }}*/}
				{/*	animate={{ scale: 1.2 }}*/}
				{/*	transition={{ duration: 0.5, yoyo: Infinity }}*/}
				{/*>*/}
				{/*	/!* Ваш SVG или иконка голоса *!/*/}
				{/*	/!* Например: *!/*/}
				{/*	/!* <img src="/voice-icon.svg" alt="Voice Icon" /> *!/*/}
				{/*</motion.div>*/}
				<div className="App">
					<header className="App-header">
						<p style={{ fontSize: '1.5em' }}>Прочитайте этот текст: </p>
						{sentencesCollections[currentCollectionIndex].map((sentence: string, index: number) => (
							<p key={index}>
								{renderHighlightedText(sentence, transcription)}
							</p>
						))}
						<br />
						{transcription &&
							<p style={{ fontSize: '1.2em' }}>Распознанный текст: {transcription}</p>
						}
						{accuracy.wer !== null && accuracy.cer !== null && accuracy.mer!== null && accuracy.wil!== null && (
							<>
								<p style={{ fontSize: '1.2em' }}>Метрика WER: {accuracy.wer}</p>
								<p style={{ fontSize: '1.2em' }}>Метрика CER: {accuracy.cer}</p>
								<p style={{ fontSize: '1.2em' }}>Метрика MER: {accuracy.mer}</p>
								<p style={{ fontSize: '1.2em' }}>Метрика WIL: {accuracy.wil}</p>
							</>
						)}
						<button onClick={startRecording} disabled={isRecording}>
							{isRecording ? 'Идет запись...' : 'Начать запись'}
						</button>
						{!isRecording && <button onClick={switchCollection}>
							Переключить коллекцию
						</button>}
					</header>
				</div>
			</div>
		</div>
	);
}