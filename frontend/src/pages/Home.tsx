import QueryInput from "../components/QueryInput";
import { useState, useRef, useEffect, useMemo } from "react";
import QuestionCard from "../components/QuestionCard";
import type { LmmResponse, RagQuestion } from "../types/rag";
import AnswerCard from "../components/AnswerCard";
import { configureHandleError, configureHandleMessage, createWebSocket, sendQuestion } from "../lib/websocket";
import Header from "@/components/Header";
import { useAppContext } from "@/contexts/AppContext";
import { toast } from "sonner";

/**Página Principal */
export default function Home(){
    const { setRagServerConnected } = useAppContext();
    const [question, setQuestion] = useState("");
    const [chatInProgress, setChatInProgress] = useState(false);
    const [ragQuestions, setRagQuestions] = useState<RagQuestion[]>([]);
    const [lmmResponses, setLmmResponses] = useState<LmmResponse[]>([]);
    const ragConversationsScrollRef = useRef<HTMLDivElement>(null);
    const ws = useRef<WebSocket | null>(null);
    const lastQuestion = useMemo(() => {
        return  ragQuestions[ragQuestions.length - 1];
    }, [ragQuestions]);

    useEffect(() => {
        ws.current = createWebSocket({ 
            setRagServerConnected, 
            onOpenCallback: () => {
                toast.info("Conexão estabelecida com o servidor de RAG");
            },
            onCloseCallback: (event) => {
                const { code, wasClean } = event;

                const codeMessages: Record<number, string> = {
                    1000: "Conexão encerrada com o servidor de RAG",
                    1001: "Servidor de RAG indisponível ou navegação interrompida",
                    1002: "Erro de protocolo durante conexão com o servidor de RAG",
                    1003: "Tipo de dado não suportado pelo servidor de RAG",
                    1006: "Conexão interrompida com o servidor de RAG",
                    1007: "Dados inválidos recebidos do servidor de RAG",
                    1008: "Violação de política do servidor de RAG",
                    1009: "Mensagem muito grande recebida do servidor de RAG",
                    1011: "Erro interno do servidor de RAG",
                };

                if (codeMessages[code]) {
                    toast.info(codeMessages[code]);
                    return;
                }

                if (!wasClean) {
                    toast.info(`Conexão encerrada inesperadamente com o servidor de RAG: (${code})`);
                    return;
                }

                toast.info("Conexão encerrada inesperadamente com o servidor de RAG");
            },
            errorCallback: (err) => {
                toast.error(`Erro inesperado durante estabelecimento da conexão com o servidor de RAG: ${err}`);
            }
        });

        configureHandleMessage({ 
            ws: ws.current, 
            setLmmResponses: setLmmResponses,
            setChatInProgress,
            ragServerErrorCallback: (errorMessage) => {
                toast.info(`Erro durante processamento da mensagem do servidor de RAG: ${errorMessage}`);
            },
            errorCallback: (err) => {
                toast.error(`Erro inesperado durante processamento da mensagem do servidor de RAG: ${err}`);
            }
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
                    setChatInProgress,
                    errorCallback: (err) => {
                        toast.error(`Erro inesperado durante envio da pergunta para o servidor de RAG: ${err}`);
                    }
                });
            }
        };

        handleSend();

    }, [lastQuestion])

    return (
        <div className="flex flex-col items-center p-4 h-screen">
            <Header />
            
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
                    <QueryInput value={question} setValue={setQuestion} chatInProgress={chatInProgress} setRagQuestions={setRagQuestions} className="shadow-lg"/>
                </div>
            </main>

        </div>
    )
}