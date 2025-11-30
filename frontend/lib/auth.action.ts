"use server";

import { cookies } from "next/headers";
import { jwtDecode } from "jwt-decode";

// Backend API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Types
export interface SignUpParams {
  username: string;
  password: string;
}

export interface SignInParams {
  username: string;
  password: string;
}

export interface User {
  username: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  token?: string;
}

// Session duration (1 week)
const SESSION_DURATION = 60 * 60 * 24 * 7;

// Set session cookie with JWT token
async function setSessionCookie(token: string) {
  const cookieStore = await cookies();

  // Set cookie in the browser
  cookieStore.set("session", token, {
    maxAge: SESSION_DURATION,
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    path: "/",
    sameSite: "lax",
  });
}

// Sign up user
export async function signUp(params: SignUpParams): Promise<AuthResponse> {
  const { username, password } = params;

  try {
    console.log("Attempting to register user:", { username, apiUrl: API_BASE_URL });
    
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });

    let data;
    try {
      data = await response.json();
    } catch (jsonError) {
      console.error("Failed to parse response as JSON:", jsonError);
      const text = await response.text();
      console.error("Response text:", text);
      return {
        success: false,
        message: `Server error: ${response.status} ${response.statusText}`,
      };
    }

    console.log("Registration response:", { status: response.status, data });

    if (!response.ok) {
      return {
        success: false,
        message: data.detail || data.message || `Failed to create account (${response.status})`,
      };
    }

    return {
      success: true,
      message: data.message || "Account created successfully. Please sign in.",
    };
  } catch (error) {
    console.error("Error creating user:", error);
    
    if (error instanceof TypeError && error.message.includes("fetch")) {
      return {
        success: false,
        message: `Cannot connect to backend at ${API_BASE_URL}. Make sure the backend server is running.`,
      };
    }

    return {
      success: false,
      message: error instanceof Error ? error.message : "Failed to create account. Please try again.",
    };
  }
}

// Sign in user
export async function signIn(params: SignInParams): Promise<AuthResponse> {
  const { username, password } = params;

  try {
    console.log("Attempting to sign in user:", { username, apiUrl: API_BASE_URL });
    
    // Use FormData for OAuth2PasswordRequestForm
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch(`${API_BASE_URL}/token`, {
      method: "POST",
      body: formData,
    });

    let data;
    try {
      data = await response.json();
    } catch (jsonError) {
      console.error("Failed to parse response as JSON:", jsonError);
      const text = await response.text();
      console.error("Response text:", text);
      return {
        success: false,
        message: `Server error: ${response.status} ${response.statusText}`,
      };
    }

    console.log("Sign in response:", { status: response.status, hasToken: !!data.access_token });

    if (!response.ok) {
      return {
        success: false,
        message: data.detail || data.message || `Failed to log into account (${response.status})`,
      };
    }

    // Store the access token in a cookie
    if (data.access_token) {
      await setSessionCookie(data.access_token);
    }

    return {
      success: true,
      message: "Successfully signed in.",
      token: data.access_token,
    };
  } catch (error) {
    console.error("Error signing in:", error);
    
    if (error instanceof TypeError && error.message.includes("fetch")) {
      return {
        success: false,
        message: `Cannot connect to backend at ${API_BASE_URL}. Make sure the backend server is running.`,
      };
    }

    return {
      success: false,
      message: error instanceof Error ? error.message : "Failed to log into account. Please try again.",
    };
  }
}

// Sign out user by clearing the session cookie
export async function signOut() {
  const cookieStore = await cookies();
  cookieStore.set("session", "", {
    maxAge: 0,
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    path: "/",
    sameSite: "lax",
  });
}

// Get current user from session cookie
export async function getCurrentUser(): Promise<User | null> {
  const cookieStore = await cookies();

  const sessionToken = cookieStore.get("session")?.value;
  if (!sessionToken) return null;

  try {
    // Decode JWT token to get user info
    const decoded = jwtDecode<{ sub: string; exp: number }>(sessionToken);

    // Check if token is expired
    if (decoded.exp && decoded.exp * 1000 < Date.now()) {
      // Token expired - return null (cookie will be ignored)
      // Cookie deletion should be handled by explicit signOut() call
      return null;
    }

    return {
      username: decoded.sub,
    };
  } catch (error) {
    console.error("Error decoding token:", error);

    // Invalid token - return null (cookie will be ignored)
    // Cookie deletion should be handled by explicit signOut() call
    return null;
  }
}

// Check if user is authenticated
export async function isAuthenticated(): Promise<boolean> {
  const user = await getCurrentUser();
  return !!user;
}
