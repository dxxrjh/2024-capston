import Image from "next/image";
import Router from "next/router";

export default function Home() {

  const testButtonClick = () => {
    Router.push("/main")
  }

  return (
    
    <div className="flex mt-[130px] items-center flex-col" >
      <Image src="/images/logo_forrest.png" alt="logo" width={100} height={100} >
      </Image>
      <h1 className="text-green-900 text-[40px] font-bold">
        For-rest
      </h1>

      <div className="mt-[30px] space-y-6">

        <button className="flex bg-[#FFEB34] w-[348px] h-[50px] rounded-[17px] flex-row items-center justify-between"
          onClick={testButtonClick}>
          <Image src="/images/logo_kakao.svg" alt="logo" width={50} height={50} className="absolute ml-0.5">
          </Image>
          <h6 className="px-[3px] flex-1">
            카카오톡으로 로그인하기
          </h6>
        </button>

        <button className="flex bg-[#E2E2E2] w-[348px] h-[50px] rounded-[17px] flex-row items-center justify-between">
          <Image src="/images/logo_google.svg" alt="logo" width={28} height={28} className="absolute ml-3">
          </Image>
          <h6 className="px-[3px] flex-1">
            구글로 로그인하기
          </h6>
        </button>

        <button className="flex bg-[#00C746] w-[348px] h-[50px] rounded-[17px] flex-row items-center justify-between">
          <Image src="/images/logo_naver.svg" alt="logo" width={40} height={40} className="absolute ml-1.5">
          </Image>
          <h6 className="px-[3px] flex-1">
            네이버로 로그인하기
          </h6>
        </button>

      </div>
    </div>
  );
}
