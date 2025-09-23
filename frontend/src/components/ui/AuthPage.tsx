import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { useAuth } from "../../api/AuthContext";
import { registerSchema, loginSchema, type RegisterInput, type LoginInput } from "../../hooks/authSchema";


const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

const AuthPage: React.FC = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [errorMessage, setErrorMessage] = useState("");
    const navigate = useNavigate();
    const { login, register: registerUser } = useAuth();

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
        reset,
    } = useForm<RegisterInput | LoginInput>({
        resolver: zodResolver(isLogin ? loginSchema : registerSchema),
    });

    const onSubmit = async (data: RegisterInput | LoginInput) => {
        setErrorMessage("");
        try {
            if (isLogin) {
                await login(data as LoginInput);
            } else {
                await registerUser(data as RegisterInput);
            }
            reset();
            navigate("/dashboard");
        } catch (err: any) {
            if (err.response?.data?.detail) {
                setErrorMessage(err.response.data.detail);
            } else {
                setErrorMessage("Something went wrong. Try again.");
            }
        }
    };

    // Social login handlers
    const handleSocialLogin = (provider: "google" | "github") => {
        // Redirect the user to the provider's authorization page
        window.location.href = `${BACKEND_URL}/oauth/${provider}`;

    };


    return (
        <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-black via-gray-900 to-white p-6">
            <div className="w-full max-w-md rounded-2xl bg-white/10 p-8 shadow-2xl backdrop-blur-lg">
                {/* Tabs */}
                <div className="mb-8 flex justify-around border-b border-gray-700">
                    <button
                        onClick={() => {
                            setIsLogin(true),
                                reset(),
                                setErrorMessage("")
                        }}
                        className={`relative pb-2 text-lg font-semibold transition ${isLogin ? "text-cyan-400" : "text-gray-300 hover:text-gray-200"
                            }`}
                    >
                        Login
                        {isLogin && <motion.div layoutId="underline" className="absolute bottom-0 left-0 right-0 h-[2px] bg-cyan-400" />}
                    </button>
                    <button
                        onClick={() => {
                            setIsLogin(false),
                                reset(),
                                setErrorMessage("")

                        }}
                        className={`relative pb-2 text-lg font-semibold transition ${!isLogin ? "text-slate-300" : "text-gray-300 hover:text-gray-200"
                            }`}
                    >
                        Register
                        {!isLogin && <motion.div layoutId="underline" className="absolute bottom-0 left-0 right-0 h-[2px] bg-slate-300" />}
                    </button>
                </div>

                {/* Animate Forms */}
                <AnimatePresence mode="wait">
                    <motion.form
                        key={isLogin ? "login" : "register"}
                        onSubmit={handleSubmit(onSubmit)}
                        initial={{ opacity: 0, x: isLogin ? 50 : -50 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: isLogin ? -50 : 50 }}
                        transition={{ duration: 0.4 }}
                        className="space-y-4"
                    >
                        {/* Username */}
                        <div>
                            <input
                                type="text"
                                placeholder="Username"
                                {...register("username")}
                                className="w-full rounded-lg border border-gray-300 bg-white/90 p-3 text-gray-900 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500"
                            />
                            {errors.username && <p className="mt-1 text-sm text-red-400">{errors.username.message as string}</p>}
                        </div>

                        {/* Email only for register */}
                        {!isLogin && (
                            <div>
                                <input
                                    type="email"
                                    placeholder="Email"
                                    {...register("email")}
                                    className="w-full rounded-lg border border-gray-300 bg-white/90 p-3 text-gray-900 focus:border-slate-500 focus:ring-2 focus:ring-slate-500"
                                />
                                {!isLogin && "email" in errors && errors.email && (
                                    <p className="mt-1 text-sm text-red-400">{errors.email.message}</p>
                                )}              </div>
                        )}

                        {/* Password */}
                        <div>
                            <input
                                type="password"
                                placeholder="Password"
                                {...register("password")}
                                className="w-full rounded-lg border border-gray-300 bg-white/90 p-3 text-gray-900 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500"
                            />
                            {errors.password && <p className="mt-1 text-sm text-red-400">{errors.password.message as string}</p>}
                        </div>

                        {/* API Error */}
                        {errorMessage && <p className="text-center text-sm text-red-500">{errorMessage}</p>}

                        {/* Submit */}
                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className={`w-full rounded-lg ${isLogin ? "bg-cyan-600 hover:bg-cyan-700" : "bg-slate-700 hover:bg-slate-800"
                                } p-3 font-semibold text-white transition disabled:opacity-50`}
                        >
                            {isSubmitting ? "Please wait..." : isLogin ? "Login" : "Register"}
                        </button>
                        {/* Social Login */}
                        <div className="flex justify-center gap-4 mt-4">
                            <button
                                type="button"
                                onClick={() => handleSocialLogin("google")}
                                className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white/90 p-2 text-gray-800 hover:bg-gray-200"
                            >
                                <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg" alt="Google" className="h-5 w-5" />
                                Google
                            </button>
                            <button
                                type="button"
                                onClick={() => handleSocialLogin("github")}
                                className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white/90 p-2 text-gray-800 hover:bg-gray-200"
                            >
                                <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" alt="GitHub" className="h-5 w-5" />
                                GitHub
                            </button>
                        </div>
                    </motion.form>
                </AnimatePresence>
            </div>
        </div>
    );
};

export default AuthPage;
