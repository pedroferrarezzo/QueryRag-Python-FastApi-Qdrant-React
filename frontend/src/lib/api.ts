import { env } from "../config/env"
import { handleHttpResponse } from "./utils"

/** Props para ingestão de vetores */
type IngestVectorsProps = {
    file: File;
}

/** Função de envio de arquivos para ingestão de vetores */
export async function ingestVectors(props: IngestVectorsProps): Promise<void> {
    const formData = new FormData()
    formData.append("file", props.file)

    const response = await fetch(`${env.VITE_API_ENDPOINT}/ingest`, {
        method: "POST",
        body: formData,
    })

    await handleHttpResponse(response);
}