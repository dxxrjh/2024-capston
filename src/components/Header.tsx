import Image from "next/image";
import Router, { useRouter } from "next/router";

const Header = () => {
  const router = useRouter()

  const logoButtonClick = () => {
    router.push("/main")
  }

  const logoutButtonClick = () => {
    router.push("/")
    // 로그인 쿠키 삭제
  }

  return (
    <div className="flex mt-[40px] flex-row w-screen justify-between">
      <div className="flex items-center ml-[40px]">
        <button>
          <Image src="/images/icon_chatbot.svg" alt="logo" width={30} height={30}
          >
          </Image>
        </button>
      </div>


      <div>
        <button
          onClick={logoButtonClick}
          className="w-[400px] flex flex-row justify-center">
          <Image src="/images/logo_forrest.png" alt="logo" width={50} height={50}
          >
          </Image>
          <h1 className="text-green-900 text-[32px] font-bold px-[5px]">
            For-rest
          </h1>
        </button>
      </div>


      <div className="flex items-center mr-[40px]">
        <button onClick={logoutButtonClick}>
          <Image src="/images/icon_logout.svg" alt="logo" width={30} height={30}
          >
          </Image>
        </button>

        <div className="mr-[20px]"></div>

        <button>
          <Image src="/images/icon_mypage.svg" alt="logo" width={30} height={30}
          >
          </Image>
        </button>
      </div>
    </div>

  );
}

export default Header;