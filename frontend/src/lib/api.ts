import type { IngestResult, RagQuestion } from "@/types/rag";
import { env } from "../config/env"
import { handleHttpResponse } from "./utils"
import { DocumentSchema, IngestResultSchema } from "@/types/schemas";
import { type Document } from "@/types/rag";

/** Props para ingestão de vetores */
type IngestVectorsProps = {
    file: File;
}

/** Props para pesquisa de vetores */
type SearchVectorsProps = {
    ragQuestion: RagQuestion
}

/** Função de envio de arquivos para ingestão de vetores */
export async function ingestVectors(props: IngestVectorsProps): Promise<IngestResult> {
    const formData = new FormData()
    formData.append("file", props.file)

    const response = await fetch(`${env.VITE_API_ENDPOINT}/vectors/ingest`, {
        method: "POST",
        body: formData,
    })

    return await handleHttpResponse({response, schema: IngestResultSchema});
}

/** Função de envio de arquivos para ingestão de vetores */
export async function searchVectors(props: SearchVectorsProps): Promise<Document[]> {
    const formData = new FormData()

    if (props.ragQuestion.question instanceof Blob) {
        formData.append("file", props.ragQuestion.question)
    }
    else if (typeof props.ragQuestion.question === "string") {
        formData.append("prompt", props.ragQuestion.question)
    }

    const response = await fetch(`${env.VITE_API_ENDPOINT}/vectors/query`, {
        method: "POST",
        body: formData,
    })

    return await handleHttpResponse({response, schema: DocumentSchema.array()});
}