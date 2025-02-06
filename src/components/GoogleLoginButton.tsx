import { GoogleOAuthProvider, useGoogleLogin } from "@react-oauth/google";
import axios from "axios";
import { useState } from "react";

const GoogleLoginButton = () => {
  const [user, setUser] = useState(null);
  //const clientID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;

  // ✅ Authorization Code 요청
  const login = useGoogleLogin({
    flow: "auth-code", // Authorization Code Flow 활성화
    onSuccess: async (codeResponse) => {
      console.log("Authorization Code:", codeResponse.code);

      try {
        const res = await axios.post("http://localhost:4000/auth/google", {
          code: codeResponse.code
        });

        localStorage.setItem("jwt", res.data.token);
        setUser(res.data.user);
      } catch (error) {
        console.error("서버 인증 실패", error);
      }
    },
    onError: () => console.log("로그인 실패"),
  });

  return (
    <div>
      {user ? (
        <div>
          <p>환영합니다, {user.name}님!</p>
          <button
            onClick={() => {
              localStorage.removeItem("jwt");
              setUser(null);
            }}
          >
            로그아웃
          </button>
        </div>
      ) : (
        <button onClick={() => login()}>Google 로그인</button>
      )}
    </div>
  );
};

export default function GoogleLoginWrapper() {
  return (
    <GoogleOAuthProvider clientId={process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID}>
      <GoogleLoginButton />
    </GoogleOAuthProvider>
  );
}