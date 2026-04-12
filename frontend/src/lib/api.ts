import type { IngestResult } from "@/types/rag";
import { env } from "../config/env"
import { handleHttpResponse } from "./utils"
import { IngestResultSchema } from "@/types/schemas";

/** Props para ingestão de vetores */
type IngestVectorsProps = {
    file: File;
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