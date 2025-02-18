import { GoogleOAuthProvider, useGoogleLogin } from "@react-oauth/google";
import axios from "axios";
import { useState } from "react";
import { useRouter } from "next/router";

const GoogleLoginButton = ({ setUser }: { setUser: (user: any) => void }) => {
  const clientID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;
  const router = useRouter()

  if (!clientID) {
    console.error("NEXT_PUBLIC_GOOGLE_CLIENT_ID가 설정되지 않았습니다.");
    return null;
  } else {
    console.log("clientID 있음");
  }


  // ✅ Authorization Code 요청
  const login = useGoogleLogin({
    flow: "auth-code",
    onSuccess: async (codeResponse) => {
      console.log("~~Authorization Code:", codeResponse.code);

      try {
        const res = await axios.post("http://localhost:3001/auth/google", {
          code: codeResponse.code
        });

        localStorage.setItem("jwt", res.data.token);
        setUser(res.data.user);

        router.push("/auth/google/callback")
      } catch (error) {
        console.error("서버 인증 실패", error);
      }
    },
    onError: () => console.log("로그인 실패"),
  });

  return (
    <button onClick={() => login()}>Google 로그인</button>
  );
};

export default function GoogleLoginWrapper({ setUser }: { setUser: (user: any) => void }) {
  console.log("GoogleOAuthProvider Client ID:", process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID); // 👀 콘솔 확인
  return (
    <GoogleOAuthProvider clientId={process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID}>
      <GoogleLoginButton setUser={setUser} />
    </GoogleOAuthProvider>
  );
}