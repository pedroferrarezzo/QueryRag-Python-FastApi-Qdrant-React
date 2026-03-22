import ThemeToggle from "./components/ThemeToggle";
import queryRagLogo from './assets/query-reg-logo.png';
import QueryInput from "./components/QueryInput";
import { useState, useRef, useEffect } from "react";
import QuestionCard from "./components/QuestionCard";
import type { RagConversation } from "./types/rag-conversation";

export default function App(){
    const [question, setQuestion] = useState("");
    const [ragConversations, setRagConversations] = useState<RagConversation[]>([]);
    const [searchIsTriggered, setSearchIsTriggered] = useState(false);
    const ragConversationsScrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (ragConversationsScrollRef.current) {
            ragConversationsScrollRef.current.scrollTo({
                top: ragConversationsScrollRef.current.scrollHeight,
                behavior: "smooth"
            });
        }
    }, [ragConversations]);

    return (
        <div className="flex flex-col items-center p-4 h-screen">
            <header className="flex justify-between w-full">
                <img 
                src={queryRagLogo} 
                alt="Descrição" 
                className="h-[clamp(55px,8vw,85px)] w-auto"
                />
                <ThemeToggle></ThemeToggle>
            </header>

            <main className={`flex-grow flex flex-col ${searchIsTriggered ? 'justify-between' : 'justify-center'} w-full max-w-4xl overflow-hidden`}>
                <div className="overflow-y-auto p-1" ref={ragConversationsScrollRef}>
                    {ragConversations.map((ragConversation, index) => {
                        const isLast = index === ragConversations.length - 1;

                        return (
                            <div key={index} className={`${isLast ? 'h-full' : 'mb-30'}`}>
                                <QuestionCard 
                                    question={ragConversation.question} 
                                    className="w-full max-w-xl ml-auto"
                                />
                                <p className="break-words mt-10">asdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsadasdsad</p>
                            </div>
                        )    
                })}
                </div>
                
                <div className="mt-3">
                    <QueryInput value={question} setValue={setQuestion} setSearchIsTriggered={setSearchIsTriggered} setRagConversations={setRagConversations} className="shadow-lg"/>
                </div>
            </main>

        </div>
    )
}