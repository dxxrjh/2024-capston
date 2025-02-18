import { GoogleOAuthProvider } from "@react-oauth/google";

const GoogleLoginButton = () => {
  const clientID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;
  const redirectURI = "http://localhost:3000/auth/google/callback"; // 리디렉션 URI

  if (!clientID) {
    console.error("NEXT_PUBLIC_GOOGLE_CLIENT_ID가 설정되지 않았습니다.");
    return null;
  }

  // 구글 로그인 페이지 URL 생성
  const googleLoginPage = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientID}&redirect_uri=${redirectURI}&response_type=code&scope=email profile`;

  return (
    <a href={googleLoginPage}>
      <button>Google 로그인</button>
    </a>
  );
};

export default function GoogleLoginWrapper() {
  return (
    <GoogleOAuthProvider clientId={process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID}>
      <GoogleLoginButton />
    </GoogleOAuthProvider>
  );
}