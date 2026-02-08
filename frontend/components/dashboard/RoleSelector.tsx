"use client"

import { useState } from "react"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import { apiRequest } from "@/lib/api"
import { useRouter } from "next/navigation"

const PREDEFINED_ROLES = [
    { title: "Frontend Developer", desc: "Master React, Vue, HTML/CSS" },
    { title: "Backend Developer", desc: "Python, Java, Node.js APIs" },
    { title: "Full Stack Developer", desc: "End-to-end web mastery" },
    { title: "Data Analyst", desc: "SQL, Python, Visualization" },
    { title: "Data Scientist", desc: "ML, Statistics, Big Data" },
    { title: "AI / ML Engineer", desc: "TensorFlow, PyTorch, LLMs" },
    { title: "DevOps Engineer", desc: "CI/CD, Docker, Kubernetes" },
    { title: "Cloud Engineer", desc: "AWS, Azure, GCP Architect" },
    { title: "Cybersecurity Analyst", desc: "SecOps, Penetration Testing" },
    { title: "UI/UX Designer", desc: "Figma, User Research, Prototyping" },
    { title: "Mobile App Developer", desc: "iOS, Android, React Native" },
    { title: "SAP ABAP Developer", desc: "Enterprise ERP Solutions" },
    { title: "Business Analyst", desc: "Agile, Requirements, Strategy" },
    { title: "Product Manager", desc: "Roadmap, Strategy, Market Fit" },
    { title: "QA Engineer", desc: "Manual & Automated Testing" },
    { title: "Automation Tester", desc: "Selenium, Cypress, Playwright" },
    { title: "Blockchain Developer", desc: "Solidity, Web3, Smart Contracts" },
    { title: "Game Developer", desc: "Unity, Unreal, C#, C++" },
    { title: "Embedded Systems Engineer", desc: "IoT, C, Microcontrollers" },
    { title: "Software Tester", desc: "Quality Assurance Fundamentals" },
]

export function DashboardRoleSelector({ onRoadmapCreated }: { onRoadmapCreated: () => void }) {
    const [loadingRole, setLoadingRole] = useState<string | null>(null)
    const [duration, setDuration] = useState<number>(6)
    const router = useRouter()

    const handleSelectRole = async (role: string) => {
        setLoadingRole(role)
        try {
            await apiRequest("/roadmaps/", {
                method: "POST",
                body: {
                    role_title: role,
                    duration_weeks: duration
                }
            })
            onRoadmapCreated()
            // Optional: navigate to specific roadmap or just reload dashboard state
        } catch (error: any) {
            console.error(error)
            alert(`Failed to generate roadmap: ${error.message || "Unknown error"}`)
        } finally {
            setLoadingRole(null)
        }
    }

    return (
        <section>
            <div className="text-center mb-10">
                <h2 className="text-3xl font-bold tracking-tight mb-2">Choose Your Career Path</h2>
                <p className="text-muted-foreground max-w-2xl mx-auto mb-6">
                    Select a role to instantly generate a personalized, AI-powered learning roadmap.
                    Start your journey to becoming a professional.
                </p>

                <div className="flex flex-col items-center gap-3">
                    <span className="text-sm font-medium text-muted-foreground">Select Duration:</span>
                    <div className="flex flex-wrap justify-center gap-2">
                        {[1, 2, 3, 4, 6].map((w) => (
                            <Button
                                key={w}
                                variant={duration === w ? "default" : "outline"}
                                onClick={() => setDuration(w)}
                                size="sm"
                                disabled={!!loadingRole}
                            >
                                {w} Weeks
                            </Button>
                        ))}
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {PREDEFINED_ROLES.map((role) => (
                    <Card
                        key={role.title}
                        className={`cursor-pointer transition-all hover:scale-105 hover:border-primary/50 bg-card ${loadingRole === role.title ? 'ring-2 ring-primary animate-pulse' : ''}`}
                        onClick={() => !loadingRole && handleSelectRole(role.title)}
                    >
                        <CardHeader>
                            <CardTitle className="text-lg">{role.title}</CardTitle>
                            <CardDescription>{role.desc}</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <Button
                                className="w-full"
                                variant={loadingRole === role.title ? "default" : "secondary"}
                                disabled={!!loadingRole}
                            >
                                {loadingRole === role.title ? "Generating AI Plan..." : `Generte ${duration}-Week Plan`}
                            </Button>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </section>
    )
}
