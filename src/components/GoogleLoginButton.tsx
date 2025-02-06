import { GoogleOAuthProvider, useGoogleLogin } from "@react-oauth/google";
import axios from "axios";
import { useState } from "react";

const GoogleLoginButton = () => {
  const [user, setUser] = useState(null);

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
    <GoogleOAuthProvider clientId="702456507747-0l5t6008oh805kii9kob01f4jhkelsg7.apps.googleusercontent.com">
      <GoogleLoginButton />
    </GoogleOAuthProvider>
  );
}