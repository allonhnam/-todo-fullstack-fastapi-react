"use client";

import { Button } from "@/components/ui/button";
import { signOut } from "@/lib/auth.action";
import { useRouter } from "next/navigation";
import { useState } from "react";

const SignOutButton = () => {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleSignOut = async () => {
    setIsLoading(true);
    try {
      await signOut();
      router.push("/");
      router.refresh(); // Refresh to update the page state
    } catch (error) {
      console.error("Error signing out:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Button
      onClick={handleSignOut}
      disabled={isLoading}
      variant="outline"
      size="lg"
    >
      {isLoading ? "Signing out..." : "Sign Out"}
    </Button>
  );
};

export default SignOutButton;

