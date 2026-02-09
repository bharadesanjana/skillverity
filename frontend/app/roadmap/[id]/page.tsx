"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { apiRequest } from "@/lib/api"
import { Button } from "@/components/ui/Button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card"
import Link from "next/link"
import { VerificationModal } from "@/components/dashboard/VerificationModal"

export default function RoadmapDetailPage() {
    const params = useParams()
    const router = useRouter()
    const [roadmap, setRoadmap] = useState<any>(null)
    const [loading, setLoading] = useState(true)

    // State for Verification Modal
    const [verifyOpen, setVerifyOpen] = useState(false)
    const [selectedWeek, setSelectedWeek] = useState<{
        week: number,
        title: string,
        skills: string[],
        tasks: string[]
    } | null>(null)

    // Store SQL items for status tracking
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

    const handleVerify = (week: any) => {
        // Extract skills and tasks for context
        // backend "weeks" structure: { week, title, skills: [], tasks: [ {task, difficulty} ] }
        const skills = week.skills || week.topics || []

        // tasks can be strings (legacy) or objects (new)
        let taskDescriptions: string[] = []
        if (Array.isArray(week.tasks)) {
            taskDescriptions = week.tasks.map((t: any) => {
                if (typeof t === 'string') return t
                return t.task // New object structure
            })
        } else if (Array.isArray(week.practice)) {
            taskDescriptions = week.practice
        }

        setSelectedWeek({
            week: week.week,
            title: week.title || week.focus,
            skills,
            tasks: taskDescriptions
        })
        setVerifyOpen(true)
    }

    if (loading) return <div className="flex h-screen items-center justify-center">Loading Roadmap...</div>
    if (!roadmap) return <div className="flex h-screen items-center justify-center">Roadmap not found</div>

    // flexible Key: weeks (new) or roadmap (legacy)
    const weeks = roadmap.content?.weeks || roadmap.content?.roadmap || []

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
                    // SQL Title format: "Week {num}: {title}"
                    const sqlItem = items.find((i: any) => i.title.startsWith(`Week ${week.week}:`))
                    const isVerified = sqlItem?.status === 'verified'

                    // Flexible field names
                    const title = week.title || week.focus
                    const skills = week.skills || week.topics || []
                    const tasks = week.tasks || week.practice || []

                    return (
                        <Card key={index} className={`border-l-4 ${isVerified ? 'border-l-green-500' : 'border-l-primary'}`}>
                            <CardHeader>
                                <CardTitle className="text-xl flex justify-between items-center">
                                    <span>Week {week.week}: {title}</span>
                                    {isVerified ? (
                                        <span className="text-sm font-bold px-3 py-1 bg-green-100 text-green-700 rounded-full">✓ Verified</span>
                                    ) : (
                                        <Button size="sm" onClick={() => handleVerify(week)}>
                                            Verify Skill
                                        </Button>
                                    )}
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div>
                                    <h4 className="font-semibold text-sm mb-1 text-primary">Key Skills</h4>
                                    <div className="flex flex-wrap gap-2">
                                        {skills.map((skill: string, i: number) => (
                                            <span key={i} className="px-2 py-1 bg-secondary/50 rounded text-sm">{skill}</span>
                                        ))}
                                    </div>
                                </div>

                                <div>
                                    <h4 className="font-semibold text-sm mb-1 text-primary">Practical Tasks</h4>
                                    <ul className="space-y-2 mt-2">
                                        {tasks.map((task: any, i: number) => {
                                            if (typeof task === 'string') {
                                                return <li key={i} className="text-sm text-muted-foreground list-disc list-inside">{task}</li>
                                            }
                                            // New Object Structure
                                            return (
                                                <li key={i} className="text-sm border p-2 rounded bg-background/50">
                                                    <div className="flex justify-between mb-1">
                                                        <span className="font-medium">{task.task}</span>
                                                        <span className={`text-xs px-2 py-0.5 rounded ${task.difficulty === 'Hard' ? 'bg-red-100 text-red-700' :
                                                                task.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                                                                    'bg-green-100 text-green-700'
                                                            }`}>{task.difficulty}</span>
                                                    </div>
                                                    <p className="text-xs text-muted-foreground">Expected: {task.expected_output}</p>
                                                </li>
                                            )
                                        })}
                                    </ul>
                                </div>

                                <div>
                                    <h4 className="font-semibold text-sm mb-1 text-primary">Outcome</h4>
                                    <p className="text-sm text-muted-foreground">{week.outcome}</p>
                                </div>
                            </CardContent>
                        </Card>
                    )
                })}

                {/* Final Assessment Card */}
                <Card className="border-l-4 border-l-purple-500 mt-8 opacity-75">
                    <CardHeader>
                        <CardTitle className="text-xl">Final Certification Exam</CardTitle>
                        <CardDescription>Complete all weekly verifications to unlock the final exam.</CardDescription>
                    </CardHeader>
                </Card>
            </div>

            {selectedWeek && (
                <VerificationModal
                    isOpen={verifyOpen}
                    onClose={() => setVerifyOpen(false)}
                    role={roadmap.role_title}
                    weekNumber={selectedWeek.week}
                    weekTitle={selectedWeek.title}
                    skills={selectedWeek.skills}
                    tasks={selectedWeek.tasks}
                    onVerified={() => {
                        alert("Skill Verified! Great job.")
                        setVerifyOpen(false)
                        // In a real app, we'd update the backend status here
                        window.location.reload()
                    }}
                />
            )}
        </div>
    )
}
