import "./Hamburger.sass"

export default function Hamburger({ isOpen, setIsOpen }: { isOpen: boolean; setIsOpen: React.Dispatch<React.SetStateAction<boolean>> }) {
	return (
		<div className={"hamburger-wrapper " + (isOpen ? "open" : "")} onClick={() => setIsOpen(!isOpen)}>
			<span className="line-1"></span>
			<span className="line-2"></span>
			<span className="line-3"></span>
		</div>
	);
}
