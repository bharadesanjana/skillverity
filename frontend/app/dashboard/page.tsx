"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/Button"
import { apiRequest } from "@/lib/api"
import { ProgressSummary, NextActionCard, RoadmapCard } from "@/components/dashboard/DashboardWidgets"
import { DashboardRoleSelector } from "@/components/dashboard/RoleSelector"

interface DashboardData {
    active_roadmaps: number
    skills_completed: number
    total_skills: number
    overall_progress: number
    streak: number
    readiness_score: number
    next_action: any
    badges: any[]
}

export default function DashboardPage() {
    const router = useRouter()
    const [summary, setSummary] = useState<DashboardData | null>(null)
    const [roadmaps, setRoadmaps] = useState<any[]>([])
    const [loading, setLoading] = useState(true)

    const loadDashboard = async () => {
        try {
            const token = localStorage.getItem("access_token")
            if (!token) {
                router.push("/login")
                return
            }

            // Parallel fetch
            const [summaryData, roadmapsData] = await Promise.all([
                apiRequest("/dashboard/summary"),
                apiRequest("/roadmaps")
            ])

            setSummary(summaryData)
            setRoadmaps(roadmapsData)

        } catch (error) {
            console.error("Dashboard Load Error:", error)
            // If 401, middleware or apiRequest should handle, but fallback:
            // router.push("/login")
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        loadDashboard()
    }, [router])

    if (loading) {
        return (
            <div className="flex flex-col h-screen items-center justify-center space-y-4">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
                <p className="text-muted-foreground animate-pulse">Consulting AI Career Coach...</p>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-background flex flex-col">
            {/* Header */}
            <header className="px-6 h-16 flex items-center border-b border-border/40 bg-background/95 backdrop-blur sticky top-0 z-50">
                <div className="flex items-center gap-2 font-bold text-xl text-primary">
                    SkillVerity
                </div>
                <div className="ml-auto flex gap-4">
                    {roadmaps.length > 0 && <Button variant="ghost" onClick={() => setRoadmaps([])}>Browse Roles</Button>}
                    <Button variant="outline" onClick={() => {
                        localStorage.removeItem("access_token")
                        router.push("/login")
                    }}>Logout</Button>
                </div>
            </header>

            <main className="container mx-auto py-8 px-6 space-y-8">
                {roadmaps.length === 0 ? (
                    <DashboardRoleSelector onRoadmapCreated={loadDashboard} />
                ) : (
                    <>
                        {/* 1. Progress Summary */}
                        <section>
                            <h2 className="text-2xl font-bold tracking-tight mb-4">Your Progress</h2>
                            <ProgressSummary stats={summary} />
                        </section>

                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                            {/* 2. Main Content: Next Action & Roadmaps */}
                            <div className="lg:col-span-2 space-y-8">
                                <section>
                                    <h3 className="text-lg font-semibold mb-3">Up Next</h3>
                                    <NextActionCard action={summary?.next_action} />
                                </section>

                                <section>
                                    <div className="flex items-center justify-between mb-4">
                                        <h3 className="text-lg font-semibold">Active Roadmaps</h3>
                                    </div>
                                    <div className="grid gap-4 sm:grid-cols-2">
                                        {roadmaps.map(r => <RoadmapCard key={r.id} roadmap={r} />)}
                                    </div>
                                </section>
                            </div>

                            {/* 3. Sidebar: Readiness & Badges */}
                            <div className="space-y-8">
                                <section>
                                    <h3 className="text-lg font-semibold mb-3">Resume Readiness</h3>
                                    <div className="bg-card border rounded-xl p-6 flex flex-col items-center text-center">
                                        <div className="relative w-32 h-32 flex items-center justify-center rounded-full border-8 border-primary/20 mb-4">
                                            <span className="text-3xl font-bold">{summary?.readiness_score}%</span>
                                            <div className="absolute inset-0 rounded-full border-8 border-t-primary border-r-transparent border-b-transparent border-l-transparent rotate-45"></div>
                                        </div>
                                        <p className="text-sm text-muted-foreground mb-4">
                                            You are {summary?.readiness_score}% ready for your target roles.
                                        </p>
                                        <Button className="w-full">Improve Resume</Button>
                                    </div>
                                </section>

                                <section>
                                    <h3 className="text-lg font-semibold mb-3">Recent Badges</h3>
                                    <div className="space-y-3">
                                        {summary?.badges.length === 0 && <div className="text-sm text-muted-foreground">No badges earned yet.</div>}
                                        {summary?.badges.map((b, i) => (
                                            <div key={i} className="flex items-center gap-3 p-3 bg-card border rounded-lg">
                                                <div className="w-8 h-8 rounded-full bg-yellow-500/20 flex items-center justify-center text-yellow-600">★</div>
                                                <div>
                                                    <div className="font-medium text-sm">{b.name}</div>
                                                    <div className="text-xs text-muted-foreground">{b.awarded_at}</div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </section>
                            </div>
                        </div>
                    </>
                )}
            </main>
        </div>
    )
}
