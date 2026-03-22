import { Card, CardContent } from "@/components/ui/card"

type Props = {
  question: string,
  className?: string
}

export default function QuestionCard({ question, className }: Props) {
  return (
    <Card className={className}>
      <CardContent className="p-2">
        <p className="text-sm text-muted-foreground mb-2">Você</p>
        <p className="text-base leading-relaxed break-words">{question}</p>
      </CardContent>
    </Card>
  )
}