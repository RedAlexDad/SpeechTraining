import {useEffect, useState} from "react";

export function useDesktop() {
    const [isDesktopLarge, setIsDesktopLarge] = useState(window.innerWidth > 1180);
    const [isDesktopMedium, setIsDesktopMedium] = useState(window.innerWidth > 768);
    const [isMobile, setIsMobile] = useState(window.innerWidth < 420);

    const updateMedia = () => {
        setIsDesktopLarge(window.innerWidth > 1180);
        setIsDesktopMedium(window.innerWidth > 768);
        setIsMobile(window.innerWidth < 420);
    };

    useEffect(() => {
        window.addEventListener("resize", updateMedia);
        return () => window.removeEventListener("resize", updateMedia);
    });

    return {
        isDesktopMedium,
        isDesktopLarge,
        isMobile
    };
}