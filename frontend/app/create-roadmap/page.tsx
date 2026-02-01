"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { Label } from "@/components/ui/Label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card"
import { apiRequest } from "@/lib/api"

export default function CreateRoadmapPage() {
    const [role, setRole] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const router = useRouter()

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError("")

        try {
            // Direct call to backend generation
            await apiRequest("/roadmaps/", {
                method: "POST",
                body: { role_title: role }
            })

            router.push("/dashboard")

        } catch (err: any) {
            console.error(err)
            setError("Failed to generate roadmap. Please try again.")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-background flex items-center justify-center p-4">
            <Card className="max-w-md w-full">
                <CardHeader>
                    <CardTitle>Create New Roadmap</CardTitle>
                    <CardDescription>
                        Enter a job role (e.g. "Full Stack Developer", "Data Scientist") and AI will generate your personalized path.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleCreate} className="space-y-4">
                        {error && <div className="text-red-500 text-sm">{error}</div>}

                        <div className="space-y-2">
                            <Label htmlFor="role">Target Role</Label>
                            <Input
                                id="role"
                                placeholder="e.g. Python Developer"
                                value={role}
                                onChange={(e) => setRole(e.target.value)}
                                disabled={loading}
                                required
                            />
                        </div>

                        <div className="flex gap-2 justify-end">
                            <Button variant="ghost" type="button" onClick={() => router.back()}>Cancel</Button>
                            <Button type="submit" disabled={loading || !role.trim()}>
                                {loading ? "Generating Plan..." : "Generate Roadmap"}
                            </Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}
