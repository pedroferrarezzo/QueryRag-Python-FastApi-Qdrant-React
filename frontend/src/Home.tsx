import ThemeToggle from "./components/ThemeToggle";
import queryRagLogo from './assets/query-reg-logo.png';
import QueryInput from "./components/QueryInput";
import { useState, useRef, useEffect, useMemo } from "react";
import QuestionCard from "./components/QuestionCard";
import type { LmmResponse, RagQuestion } from "./types/rag";
import AnswerCard from "./components/AnswerCard";
import { configureHandleError, configureHandleMessage, createWebSocket, sendQuestion } from "./lib/websocket";
import RagServerStatus from "./components/RagServerStatus";
import type { ServerConnectionStatus } from "./types/server";

export default function Home(){
    const [question, setQuestion] = useState("");
    const [chatInProgress, setChatInProgress] = useState(false);
    const [ragServerConnected, setRagServerConnected] = useState<ServerConnectionStatus>("disconnected");
    const [ragQuestions, setRagQuestions] = useState<RagQuestion[]>([]);
    const [lmmResponses, setLmmResponses] = useState<LmmResponse[]>([]);
    const ragConversationsScrollRef = useRef<HTMLDivElement>(null);
    const ws = useRef<WebSocket | null>(null);
    const lastQuestion = useMemo(() => {
        return  ragQuestions[ragQuestions.length - 1];
    }, [ragQuestions]);

    useEffect(() => {
        ws.current = createWebSocket({ setRagServerConnected });

        configureHandleMessage({ 
            ws: ws.current, 
            setLmmResponses: setLmmResponses,
            setChatInProgress 
        });
        configureHandleError({ ws: ws.current, setChatInProgress });

        return () => {
            ws.current?.close();
            ws.current = null;
        }

    }, [])

    useEffect(() => {
        if (ragConversationsScrollRef.current) {
            ragConversationsScrollRef.current.scrollTo({
                top: ragConversationsScrollRef.current.scrollHeight,
                behavior: "smooth"
            });
        }
        
        const handleSend = async () => {
            if (ws.current && ws.current.readyState === WebSocket.OPEN && lastQuestion) {
                await sendQuestion({
                    ws: ws.current, 
                    lastQuestion: lastQuestion, 
                    setChatInProgress
                });
            }
        };

        handleSend();

    }, [lastQuestion])

    return (
        <div className="flex flex-col items-center p-4 h-screen">
            <header className="flex justify-between w-full items-center">
                <img 
                src={queryRagLogo} 
                alt="Descrição" 
                className="h-[clamp(55px,8vw,85px)] w-auto"
                />
                <RagServerStatus ragServerConnected={ragServerConnected} />
                <ThemeToggle />
            </header>

            <main className={`flex-grow flex flex-col ${ragQuestions.length > 0 ? 'justify-between' : 'justify-center'} w-full max-w-4xl overflow-hidden`}>
                <div className="overflow-y-auto p-1 scrollbar-hide" ref={ragConversationsScrollRef}>
                    {ragQuestions.map((ragQuestion, index) => {
                        const isLastQuestion = index === ragQuestions.length - 1;
                        const lmmResponse = lmmResponses.find(a => a.questionId === ragQuestion.id);

                        return (
                            <div key={index} className={`${isLastQuestion ? 'h-full' : 'mb-30'}`}>
                                <QuestionCard 
                                    ragQuestion={ragQuestion} 
                                    className="w-full max-w-xl ml-auto"
                                />
                                <AnswerCard chatInProgress={chatInProgress} lmmResponse={lmmResponse} className="break-words mt-10" isLastAnswer={isLastQuestion}></AnswerCard>
                            </div>
                        )    
                })}
                </div>
                
                <div className="mt-3">
                    <QueryInput value={question} setValue={setQuestion} chatInProgress={chatInProgress} setRagQuestions={setRagQuestions} connectionStatus={ragServerConnected} className="shadow-lg"/>
                </div>
            </main>

        </div>
    )
}