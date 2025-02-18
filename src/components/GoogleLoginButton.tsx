import { GoogleOAuthProvider } from "@react-oauth/google";
import { useState, useEffect } from "react";
import Router from "next/router";
import Cookies from "js-cookie";

const GoogleLoginButton = () => {
  const clientID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;
  const redirectURI = "http://localhost:3000/auth/google/callback"; // 리디렉션 URI
  const [isLogin, setIsLogin] = useState(false);
  const [userName, setUserName] = useState("");

  // 로그인 상태 확인
  useEffect(() => {
    const token = Cookies.get("jwt"); // 쿠키에서 jwt 토큰 확인
    if (token) {
      const decoded = JSON.parse(atob(token.split(".")[1])); // JWT 토큰 디코딩
      setUserName(decoded.name);
      setIsLogin(true);
    }
  }, []);

  // 구글 로그인 페이지 URL 생성
  const googleLoginPage = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientID}&redirect_uri=${redirectURI}&response_type=code&scope=email profile`;

  // 로그아웃 처리
  const handleLogout = () => {
    Cookies.remove("jwt"); // 쿠키에서 jwt 삭제
    setIsLogin(false);
    setUserName("");
    Router.push("/"); // 홈 페이지로 리다이렉트
  };

  if (!clientID) {
    console.error("NEXT_PUBLIC_GOOGLE_CLIENT_ID가 설정되지 않았습니다.");
    return null;
  }

  return (
    <div>
      {isLogin ? (
        <div>
          <p>{userName}님, 환영합니다!</p>
          <button onClick={handleLogout}>로그아웃</button>
        </div>
      ) : (
        <a href={googleLoginPage}>
          <button>Google 로그인</button>
        </a>
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