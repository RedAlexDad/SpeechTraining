import "./Home.sass"
import {Link} from "react-router-dom";
import { motion } from 'framer-motion';

export default function HomePage() {
	return (
		<div className="home-page-wrapper">
			<div className="voice-animation-wrapper">
				<motion.div
					className="voice-icon"
					initial={{ scale: 1 }}
					animate={{ scale: 1.2 }}
					transition={{ duration: 0.5, yoyo: Infinity }}
				>
					{/* Ваш SVG или иконка голоса */}
					{/* Например: */}
					{/* <img src="/voice-icon.svg" alt="Voice Icon" /> */}
				</motion.div>
			</div>
		</div>
	);
}