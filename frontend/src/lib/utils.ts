import { ErrorSchema } from "@/types/schemas";
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import { type ZodType  } from "zod";

/** Props para manipulação de respostas HTTP */
type handleHttpResponseProps<T> = {
    response: Response;
    schema: ZodType<T>
}

/** Função para combinar classes CSS de forma eficiente */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Converte um Blob em uma string Base64
 * @param {Blob} blob - O objeto binário (arquivo, imagem, etc)
 * @returns {Promise<string>} - A string em formato Base64
 */
export function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64String = (reader.result as string).split(',')[1];
      resolve(base64String);
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

/** Trata a resposta de APIs */
export async function handleHttpResponse<T>({ response, schema }: handleHttpResponseProps<T>): Promise<T> {
    const result = await response.json();
    if (!response.ok) {
        let errorMessage;
        try {
            const error = ErrorSchema.parse(result);
            errorMessage = error.data;
        }
        catch(err) {
            errorMessage = "Erro desconhecido durante a manipulação da resposta de erro";
        }

        throw new Error(errorMessage);
    }

    try {
      return schema.parse(result);
    }
    catch(err) {
        throw new Error("Erro desconhecido durante a manipulação da resposta de sucesso");
    }
}