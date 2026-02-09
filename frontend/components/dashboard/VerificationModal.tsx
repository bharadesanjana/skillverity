"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/Dialog"
import { Button } from "@/components/ui/Button"
import { Textarea } from "@/components/ui/Textarea"
import { apiRequest } from "@/lib/api"
import { Loader2, CheckCircle, XCircle, AlertTriangle } from "lucide-react"

interface VerificationModalProps {
    isOpen: boolean
    onClose: () => void
    role: string
    weekNumber: number
    weekTitle: string
    skills: string[]
    tasks: string[] // List of task descriptions
    onVerified: () => void
}

type Question = {
    id: number
    type: string
    question: string
    evaluation_criteria: string[]
}

type AssessmentState = "loading" | "question" | "evaluating" | "result" | "followup_loading" | "followup"

export function VerificationModal({ isOpen, onClose, role, weekNumber, weekTitle, skills, tasks, onVerified }: VerificationModalProps) {
    const [state, setState] = useState<AssessmentState>("loading")
    const [question, setQuestion] = useState<Question | null>(null)
    const [answer, setAnswer] = useState("")
    const [evaluation, setEvaluation] = useState<any>(null)
    const [followup, setFollowup] = useState<any>(null)

    // Reset state when opening
    useEffect(() => {
        if (isOpen) {
            setState("loading")
            setAnswer("")
            setEvaluation(null)
            setFollowup(null)
            generateAssessment()
        }
    }, [isOpen])

    const generateAssessment = async () => {
        try {
            const data = await apiRequest("/verification/generate", {
                method: "POST",
                body: {
                    role,
                    week: weekNumber,
                    title: weekTitle,
                    skills,
                    tasks
                }
            })

            if (data.questions && data.questions.length > 0) {
                setQuestion(data.questions[0])
                setState("question")
            } else {
                alert("Failed to generate assessment questions.")
                onClose()
            }
        } catch (error) {
            console.error(error)
            alert("Error generating assessment.")
            onClose()
        }
    }

    const submitAnswer = async () => {
        if (!question || !answer.trim()) return

        setState("evaluating")
        try {
            const data = await apiRequest("/verification/evaluate", {
                method: "POST",
                body: {
                    role,
                    week: weekNumber,
                    skill_focus: skills[0] || "General", // focused skill
                    question: question.question,
                    answer
                }
            })
            setEvaluation(data)
            setState("result")
        } catch (error) {
            console.error(error)
            alert("Error evaluating answer.")
            setState("question")
        }
    }

    const requestFollowup = async () => {
        setState("followup_loading")
        try {
            const summary = `Score: ${evaluation.score}. Strengths: ${evaluation.strengths.join(", ")}. Weaknesses: ${evaluation.weaknesses.join(", ")}.`
            const data = await apiRequest("/verification/followup", {
                method: "POST",
                body: { summary }
            })

            if (data.follow_up_question) {
                // Set as new question
                setQuestion({
                    id: 99,
                    type: "followup",
                    question: data.follow_up_question,
                    evaluation_criteria: []
                })
                setAnswer("")
                setEvaluation(null)
                setState("question")
            } else {
                alert("No follow-up generated. You are done!")
                onClose()
            }
        } catch (error: any) {
            console.error(error)
            alert("Error generating follow-up.")
            setState("result")
        }
    }

    const handleClose = () => {
        if (evaluation?.verdict === "Hire" || evaluation?.verdict === "Strong") {
            onVerified()
        }
        onClose()
    }

    return (
        <Dialog open={isOpen} onOpenChange={handleClose}>
            <DialogContent className="sm:max-w-2xl">
                <DialogHeader>
                    <DialogTitle>Skill Verification: Week {weekNumber}</DialogTitle>
                    <DialogDescription>{weekTitle}</DialogDescription>
                </DialogHeader>

                <div className="py-4">
                    {state === "loading" && (
                        <div className="flex flex-col items-center justify-center py-10 space-y-4">
                            <Loader2 className="h-8 w-8 animate-spin text-primary" />
                            <p className="text-muted-foreground">Generating practical scenario...</p>
                        </div>
                    )}

                    {state === "question" && question && (
                        <div className="space-y-4">
                            <div className="bg-secondary/20 p-4 rounded-lg border">
                                <h3 className="font-semibold mb-2 text-primary">Scenario / Question:</h3>
                                <p className="text-lg">{question.question}</p>
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium">Your Answer / Solution:</label>
                                <Textarea
                                    value={answer}
                                    onChange={(e) => setAnswer(e.target.value)}
                                    placeholder="Type your explanation, code, or design approach here..."
                                    className="h-40 font-mono text-sm"
                                />
                            </div>
                        </div>
                    )}

                    {state === "evaluating" && (
                        <div className="flex flex-col items-center justify-center py-10 space-y-4">
                            <Loader2 className="h-8 w-8 animate-spin text-primary" />
                            <p className="text-muted-foreground">AI is evaluating your response...</p>
                        </div>
                    )}

                    {state === "result" && evaluation && (
                        <div className="space-y-6">
                            <div className={`p-4 rounded-lg border flex items-start gap-4 ${evaluation.score >= 70 ? "bg-green-50 border-green-200" : "bg-red-50 border-red-200"
                                }`}>
                                {evaluation.score >= 70 ? (
                                    <CheckCircle className="h-6 w-6 text-green-600 mt-1" />
                                ) : (
                                    <XCircle className="h-6 w-6 text-red-600 mt-1" />
                                )}
                                <div>
                                    <h3 className="font-bold text-lg capitalize">{evaluation.verdict} ({evaluation.score}/100)</h3>
                                    <p className="text-sm mt-1">{evaluation.feedback}</p>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="p-3 bg-secondary/10 rounded border">
                                    <h4 className="font-semibold text-green-700 text-sm mb-2">Strengths</h4>
                                    <ul className="list-disc list-inside text-sm text-muted-foreground">
                                        {evaluation.strengths.map((s: string, i: number) => <li key={i}>{s}</li>)}
                                    </ul>
                                </div>
                                <div className="p-3 bg-secondary/10 rounded border">
                                    <h4 className="font-semibold text-red-700 text-sm mb-2">Weaknesses</h4>
                                    <ul className="list-disc list-inside text-sm text-muted-foreground">
                                        {evaluation.weaknesses.map((w: string, i: number) => <li key={i}>{w}</li>)}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    )}

                    {state === "followup_loading" && (
                        <div className="flex flex-col items-center justify-center py-10 space-y-4">
                            <Loader2 className="h-8 w-8 animate-spin text-primary" />
                            <p className="text-muted-foreground">Generating adaptive follow-up...</p>
                        </div>
                    )}
                </div>

                <DialogFooter>
                    {state === "question" && (
                        <div className="flex gap-2 w-full justify-end">
                            <Button variant="outline" onClick={onClose}>Cancel</Button>
                            <Button onClick={submitAnswer} disabled={!answer.trim()}>Submit Answer</Button>
                        </div>
                    )}

                    {state === "result" && (
                        <div className="flex gap-2 w-full justify-end">
                            <Button variant="secondary" onClick={onClose}>Finish</Button>
                            {evaluation?.score < 70 && (
                                <Button onClick={requestFollowup}>Try Follow-up Question</Button>
                            )}
                        </div>
                    )}
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
