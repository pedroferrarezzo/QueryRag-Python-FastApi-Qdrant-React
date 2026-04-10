import ThemeToggle from "../components/ThemeToggle";
import queryRagLogo from '../assets/query-reg-logo.png';
import RagServerStatus from "../components/RagServerStatus";
import { useAppContext } from "@/contexts/AppContext";
import { NavigationMenu } from "./Menu";

/** Props para o componente Header */
type HeaderProps = {
    className?: string;
}

/**Componente de Cabeçalho */
export default function Header(props: HeaderProps){
    const { ragServerConnected } = useAppContext();
    return (
        <header className={`flex justify-between w-full items-center ${props.className || ''}`}>
            <div className="flex items-center gap-1">
                <NavigationMenu />
                <img 
                    src={queryRagLogo} 
                    alt="Descrição" 
                    className="h-[clamp(55px,8vw,85px)] w-auto"
                />
            </div>
            
            <RagServerStatus ragServerConnected={ragServerConnected} />
            <ThemeToggle />
        </header>
    );
}