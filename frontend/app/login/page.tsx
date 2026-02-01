"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { Label } from "@/components/ui/Label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/Card"
import { apiRequest } from "@/lib/api"

export default function LoginPage() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)
    const router = useRouter()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        console.log("[Login] Form Submitted")
        setError("")
        setLoading(true)

        try {
            // Backend expects 'username' and 'password' as URL-encoded form data for OAuth2
            // But let's check our API implementation.
            // In auth.py: login(form_data: OAuth2PasswordRequestForm = Depends())
            // This requires x-www-form-urlencoded body.

            const formData = new URLSearchParams()
            formData.append("username", email)
            formData.append("password", password)

            console.log("[Login] Sending credentials for:", email)

            // We explicitly set Content-Type in options to override JSON default in apiRequest
            // Or we can manually fetch here to avoid apiRequest strict JSON behavior if needed.
            // Let's modify apiRequest usage or handle it here.
            // Since apiRequest defaults to JSON, let's use fetch directly for this specific OAuth endpoint
            // OR update apiRequest. Let's use fetch directly here for clarity and control over FormData.

            const res = await fetch("http://127.0.0.1:8000/token", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: formData.toString()
            })

            const data = await res.json()

            if (!res.ok) {
                throw new Error(data.detail || "Login failed")
            }

            console.log("[Login] Success, received token")
            localStorage.setItem("token", data.access_token)
            router.push("/dashboard")

        } catch (err: any) {
            console.error("[Login] Error:", err)
            setError(err.message || "Login failed. Please check your credentials.")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="flex min-h-screen items-center justify-center px-4 bg-background">
            <Card className="w-full max-w-sm">
                <CardHeader>
                    <CardTitle className="text-2xl">Login</CardTitle>
                    <CardDescription>
                        Enter your email below to login to your account.
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent className="grid gap-4">
                        {error && (
                            <div className="bg-destructive/15 text-destructive text-sm p-3 rounded-md">
                                {error}
                            </div>
                        )}
                        <div className="grid gap-2">
                            <Label htmlFor="email">Email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="m@example.com"
                                required
                                disabled={loading}
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                        <div className="grid gap-2">
                            <Label htmlFor="password">Password</Label>
                            <Input
                                id="password"
                                type="password"
                                required
                                disabled={loading}
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                    </CardContent>
                    <CardFooter className="flex flex-col gap-2">
                        <Button className="w-full" type="submit" disabled={loading}>
                            {loading ? "Signing in..." : "Sign in"}
                        </Button>
                        <div className="text-center text-sm">
                            Don't have an account?{" "}
                            <Link href="/register" className="underline">
                                Sign up
                            </Link>
                        </div>
                    </CardFooter>
                </form>
            </Card>
        </div>
    )
}
