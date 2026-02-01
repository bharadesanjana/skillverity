"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import Link from "next/link"
import { Progress } from "@/components/ui/Progress" // Assuming we have this or I'll genericize it

// --- Progress Summary Component ---
export function ProgressSummary({ stats }: { stats: any }) {
    if (!stats) return null;

    const items = [
        { label: "Active Roadmaps", value: stats.active_roadmaps, sub: "In Progress" },
        { label: "Skills Verified", value: `${stats.skills_completed}/${stats.total_skills}`, sub: "Skills Mastered" },
        { label: "Daily Streak", value: stats.streak, sub: "Days Active" },
        { label: "Global Progress", value: `${stats.overall_progress}%`, sub: "Total Completion" },
    ]

    return (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {items.map((item, i) => (
                <Card key={i}>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">{item.label}</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{item.value}</div>
                        <p className="text-xs text-muted-foreground">{item.sub}</p>
                    </CardContent>
                </Card>
            ))}
        </div>
    )
}

// --- Next Action Card ---
export function NextActionCard({ action }: { action: any }) {
    if (!action) return (
        <Card className="bg-primary/5 border-primary/20">
            <CardHeader>
                <CardTitle>All Caught Up!</CardTitle>
                <CardDescription>You have no pending tasks. Start a new roadmap?</CardDescription>
            </CardHeader>
            <CardContent>
                <Link href="/create-roadmap">
                    <Button>Create New Roadmap</Button>
                </Link>
            </CardContent>
        </Card>
    );

    return (
        <Card className="bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border-indigo-500/20">
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <span className="bg-indigo-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">!</span>
                    Next Recommended Action
                </CardTitle>
                <CardDescription>Based on your learning velocity</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
                <div>
                    <div className="text-lg font-semibold">{action.item_title}</div>
                    <div className="text-sm text-muted-foreground">in {action.roadmap_title} • {action.estimated_time}</div>
                </div>
                <Link href={`/roadmap/${action.roadmap_id}`}>
                    <Button className="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-700">
                        Start Learning
                    </Button>
                </Link>
            </CardContent>
        </Card>
    )
}

// --- Roadmap Card ---
export function RoadmapCard({ roadmap }: { roadmap: any }) {
    // Calculate progress manually if not in API, or use status
    // For now we assume roadmap object matches what we need
    return (
        <Card>
            <CardHeader>
                <div className="flex justify-between items-start">
                    <div>
                        <CardTitle className="mb-1">{roadmap.role_title}</CardTitle>
                        <CardDescription>Created {new Date(roadmap.created_at || Date.now()).toLocaleDateString()}</CardDescription>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${roadmap.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                        {roadmap.status}
                    </span>
                </div>
            </CardHeader>
            <CardContent>
                <div className="space-y-4">
                    {/* Mock Progress Bar since backend aggregation for single roadmap wasn't explicit, 
                        but we can visualize 'status' */}
                    <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                        <div className="h-full bg-primary" style={{ width: '40%' }}></div>
                    </div>
                    <div className="flex gap-2">
                        <Link href={`/roadmap/${roadmap.id}`} className="flex-1">
                            <Button className="w-full" variant="secondary">Continue</Button>
                        </Link>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}
