"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { apiRequest } from "@/lib/api"
import { Button } from "@/components/ui/Button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card"
import Link from "next/link"
import { QuizModal } from "@/components/dashboard/QuizModal"

export default function RoadmapDetailPage() {
    const params = useParams()
    const router = useRouter()
    const [roadmap, setRoadmap] = useState<any>(null)
    const [loading, setLoading] = useState(true)

    // State for Quiz Modal
    const [quizOpen, setQuizOpen] = useState(false)
    const [selectedItem, setSelectedItem] = useState<{ id: number, title: string } | null>(null)
    const [items, setItems] = useState<any[]>([])

    useEffect(() => {
        const fetchRoadmap = async () => {
            try {
                const id = Array.isArray(params?.id) ? params?.id[0] : params?.id
                if (!id) return

                const data = await apiRequest(`/roadmaps/${id}`)
                setRoadmap(data)

                if (data.items) {
                    setItems(data.items)
                }
            } catch (error) {
                console.error("Failed to fetch roadmap:", error)
                alert("Failed to load roadmap details.")
                router.push("/dashboard")
            } finally {
                setLoading(false)
            }
        }
        fetchRoadmap()
    }, [params, router])

    const handleOpenQuiz = (weekNum: number, focus: string) => {
        // Find the matching SQL item
        // The title in SQL is "Week {num}: {focus}"
        const match = items.find((i: any) => i.title.startsWith(`Week ${weekNum}:`))
        if (match) {
            setSelectedItem({ id: match.id, title: match.title })
            setQuizOpen(true)
        } else {
            alert("Quiz not available for this week yet.")
        }
    }

    if (loading) return <div className="flex h-screen items-center justify-center">Loading Roadmap...</div>
    if (!roadmap) return <div className="flex h-screen items-center justify-center">Roadmap not found</div>

    const weeks = roadmap.content?.roadmap || []

    return (
        <div className="min-h-screen bg-background p-6">
            <header className="flex items-center justify-between mb-8 max-w-4xl mx-auto">
                <div>
                    <h1 className="text-3xl font-bold">{roadmap.role_title}</h1>
                    <p className="text-muted-foreground">{roadmap.duration_weeks}-Week Career Roadmap</p>
                </div>
                <Link href="/dashboard">
                    <Button variant="outline">Back to Dashboard</Button>
                </Link>
            </header>

            <div className="max-w-4xl mx-auto space-y-6">
                {weeks.map((week: any, index: number) => {
                    // Check status from items if available
                    const sqlItem = items.find((i: any) => i.title.startsWith(`Week ${week.week}:`))
                    const isVerified = sqlItem?.status === 'verified'

                    return (
                        <Card key={index} className={`border-l-4 ${isVerified ? 'border-l-green-500' : 'border-l-primary'}`}>
                            <CardHeader>
                                <CardTitle className="text-xl flex justify-between items-center">
                                    <span>Week {week.week}: {week.focus}</span>
                                    {isVerified ? (
                                        <span className="text-sm font-bold px-3 py-1 bg-green-100 text-green-700 rounded-full">✓ Verified</span>
                                    ) : (
                                        <Button size="sm" onClick={() => handleOpenQuiz(week.week, week.focus)}>
                                            Verify Skill
                                        </Button>
                                    )}
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div>
                                    <h4 className="font-semibold text-sm mb-1 text-primary">Topics</h4>
                                    <div className="flex flex-wrap gap-2">
                                        {week.topics?.map((topic: string, i: number) => (
                                            <span key={i} className="px-2 py-1 bg-secondary/50 rounded text-sm">{topic}</span>
                                        ))}
                                    </div>
                                </div>

                                <div>
                                    <h4 className="font-semibold text-sm mb-1 text-primary">Tasks</h4>
                                    <ul className="list-disc list-inside text-sm text-muted-foreground">
                                        {(week.tasks || week.practice)?.map((item: string, i: number) => (
                                            <li key={i}>{item}</li>
                                        ))}
                                    </ul>
                                </div>

                                <div>
                                    <h4 className="font-semibold text-sm mb-1 text-primary">Outcome</h4>
                                    <p className="text-sm">{week.outcome}</p>
                                </div>
                            </CardContent>
                        </Card>
                    )
                })}

                {/* Final Assessment Card */}
                {(() => {
                    const finalItem = items.find((i: any) => i.title === "Final Assessment")
                    if (finalItem) {
                        const isVerified = finalItem.status === 'verified'
                        return (
                            <Card className={`border-l-4 ${isVerified ? 'border-l-purple-500' : 'border-l-primary'} mt-8`}>
                                <CardHeader>
                                    <CardTitle className="text-xl flex justify-between items-center">
                                        <span>Final Assessment</span>
                                        {isVerified ? (
                                            <span className="text-sm font-bold px-3 py-1 bg-purple-100 text-purple-700 rounded-full">🏆 Expert Verified</span>
                                        ) : (
                                            <Button size="sm" onClick={() => {
                                                setSelectedItem({ id: finalItem.id, title: finalItem.title })
                                                setQuizOpen(true)
                                            }}>
                                                Take Final Exam
                                            </Button>
                                        )}
                                    </CardTitle>
                                    <CardDescription>
                                        Comprehensive test to verify your expertise and earn the Expert Badge.
                                    </CardDescription>
                                </CardHeader>
                            </Card>
                        )
                    }
                })()}
            </div>

            {selectedItem && (
                <QuizModal
                    isOpen={quizOpen}
                    onClose={() => setQuizOpen(false)}
                    roadmapItemId={selectedItem.id}
                    title={selectedItem.title}
                    onQuizPassed={() => {
                        alert("Skill Verified!")
                        setQuizOpen(false)
                        // Reload items to show verified status
                        window.location.reload()
                    }}
                />
            )}
        </div>
    )
}
