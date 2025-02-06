import Image from "next/image";
import Router, { useRouter } from "next/router";

export default function Main() {
  const router = useRouter()

  const searchButtonClick = () => {
    router.push("/search_result")
  }


  return (
    <div>
      <h2 className="flex flex-row justify-center mt-[20px] text-[18px] text-green-900">
        ㅇㅇㅇ 님을 위해 준비했습니다!
      </h2>

      <div className="flex flex-row items-center">
        <div className="w-[1012px] h-[59px] mx-auto flex flex-row mt-[15px] items-center bg-[#EBEBEB] rounded-[17px] pl-[30px] py-[19px] text-[14px]">
          <textarea className="resize-none w-[900px] h-[59px] bg-transparent text-[14px] outline-none px-[30px] py-[19px]"
            placeholder="어떤 여가를 더 원하시나요?">
          </textarea>

          <button onClick={searchButtonClick}>
            <Image src="/images/icon_search.svg" alt="logo" width={30} height={30} className="flex">
            </Image>
          </button>
        </div>
      </div>

      <div className="flex flex-row justify-between items-center ">

        <div>
          <button className="border border-[#EBEBEB] rounded-[17%] text-[#9A9A9A] px-4 py-2">
            카테고리
          </button>
        </div>


        <button className="border border-[#EBEBEB] rounded-[17%] text-[#9A9A9A] px-4 py-2">
          일정
        </button>

        <button className="border border-[#EBEBEB] rounded-[17%] text-[#9A9A9A] px-4 py-2">
          정렬
        </button>
      </div>


    </div>





  );
}
