"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/Dialog"
import { Button } from "@/components/ui/Button"
import { apiRequest } from "@/lib/api"
import { Loader2 } from "lucide-react"

interface Question {
    id: number
    text: string
    options: string[]
    correct_option?: number
}

interface QuizResponse {
    id: number
    questions: Question[]
    score?: number
    passed: boolean
}

interface QuizModalProps {
    isOpen: boolean
    onClose: () => void
    roadmapItemId: number
    title: string
    onQuizPassed: () => void
}

export function QuizModal({ isOpen, onClose, roadmapItemId, title, onQuizPassed }: QuizModalProps) {
    const [step, setStep] = useState<'intro' | 'loading' | 'question' | 'result'>('intro')
    const [questions, setQuestions] = useState<Question[]>([])
    const [quizId, setQuizId] = useState<number | null>(null)
    const [currentQIndex, setCurrentQIndex] = useState(0)
    const [answers, setAnswers] = useState<number[]>([]) // Stores selected option indices
    const [score, setScore] = useState<number | null>(null)
    const [passed, setPassed] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const resetState = () => {
        setStep('intro')
        setQuestions([])
        setQuizId(null)
        setCurrentQIndex(0)
        setAnswers([])
        setScore(null)
        setPassed(false)
        setError(null)
    }

    const startQuiz = async () => {
        setStep('loading')
        setError(null)
        try {
            // Fetch/Generate Quiz
            const quizData: QuizResponse = await apiRequest(`/quizzes/generate/${roadmapItemId}`, { method: "POST" })
            setQuestions(quizData.questions)
            setQuizId(quizData.id)
            setStep('question')
            setCurrentQIndex(0)
            setAnswers([])
        } catch (err: any) {
            console.error(err)
            setError(err.message || "Failed to load quiz")
            setStep('intro')
        }
    }

    const handleOptionSelect = (optionIndex: number) => {
        const newAnswers = [...answers]
        newAnswers[currentQIndex] = optionIndex
        setAnswers(newAnswers)
    }

    const handleNext = () => {
        if (currentQIndex < questions.length - 1) {
            setCurrentQIndex(currentQIndex + 1)
        } else {
            submitQuiz()
        }
    }

    const submitQuiz = async () => {
        setStep('loading')
        try {
            if (!quizId) throw new Error("Quiz ID missing")

            const result = await apiRequest(`/quizzes/${quizId}/submit`, {
                method: "POST",
                body: { answers }
            })

            setScore(result.score)
            setPassed(result.passed)
            setStep('result')

            if (result.passed) {
                onQuizPassed()
            }
        } catch (err: any) {
            console.error(err)
            setError(err.message || "Failed to submit quiz")
            setStep('result')
        }
    }

    const currentQuestion = questions[currentQIndex]
    const currentAnswer = answers[currentQIndex]

    return (
        <Dialog open={isOpen} onOpenChange={(open) => {
            if (!open) {
                onClose()
                setTimeout(resetState, 300) // Reset after close animation
            }
        }}>
            <DialogContent className="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle>Quiz: {title}</DialogTitle>
                    <DialogDescription>
                        {step === 'intro' && "Test your knowledge on this topic. Pass with >70% to verify this skill."}
                        {step === 'question' && `Question ${currentQIndex + 1} of ${questions.length}`}
                        {step === 'result' && "Quiz Results"}
                    </DialogDescription>
                </DialogHeader>

                <div className="py-4">
                    {step === 'intro' && (
                        <div className="text-center space-y-4">
                            <p>Are you ready to start?</p>
                            {error && <p className="text-red-500 text-sm">{error}</p>}
                        </div>
                    )}

                    {step === 'loading' && (
                        <div className="flex justify-center items-center py-8">
                            <Loader2 className="h-8 w-8 animate-spin text-primary" />
                            <span className="ml-2">Please wait...</span>
                        </div>
                    )}

                    {step === 'question' && currentQuestion && (
                        <div className="space-y-4">
                            <p className="font-medium text-lg">{currentQuestion.text}</p>
                            <div className="space-y-2">
                                {currentQuestion.options.map((option, idx) => (
                                    <Button
                                        key={idx}
                                        variant={currentAnswer === idx ? "default" : "outline"}
                                        className="w-full justify-start text-left h-auto py-3 px-4"
                                        onClick={() => handleOptionSelect(idx)}
                                    >
                                        <div className="flex items-center w-full">
                                            <span className="mr-3 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-primary/30 text-xs">
                                                {String.fromCharCode(65 + idx)}
                                            </span>
                                            <span className="break-words w-full whitespace-normal">{option}</span>
                                        </div>
                                    </Button>
                                ))}
                            </div>
                        </div>
                    )}

                    {step === 'result' && (
                        <div className="text-center space-y-4">
                            <div className="text-4xl font-bold mb-2">
                                {score ? Math.round(score) : 0}%
                            </div>
                            {passed ? (
                                <div className="text-green-600 font-medium">
                                    <p className="text-xl">Congratulations!</p>
                                    <p>You passed the quiz and verified this skill.</p>
                                </div>
                            ) : (
                                <div className="text-red-500 font-medium">
                                    <p className="text-xl">Keep Learning</p>
                                    <p>Review the materials and try again.</p>
                                    {error && <p className="text-sm mt-2">{error}</p>}
                                </div>
                            )}
                        </div>
                    )}
                </div>

                <DialogFooter>
                    {step === 'intro' && (
                        <Button onClick={startQuiz}>Start Quiz</Button>
                    )}

                    {step === 'question' && (
                        <Button onClick={handleNext} disabled={currentAnswer === undefined}>
                            {currentQIndex < questions.length - 1 ? "Next Question" : "Submit Quiz"}
                        </Button>
                    )}

                    {step === 'result' && (
                        <div className="flex gap-2 w-full justify-end">
                            <Button variant="outline" onClick={onClose}>Close</Button>
                            {!passed && <Button onClick={startQuiz}>Retry</Button>}
                        </div>
                    )}
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
