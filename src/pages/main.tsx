import Image from "next/image";
import Router from "next/router";

export default function Main() {

  return (
    <div>
      <h2 className="flex flex-row justify-center mt-[20px] text-[18px] text-green-900">
        ㅇㅇㅇ 님을 위해 준비했습니다!
      </h2>

      <textarea className="text-left mx-auto flex flex-row mt-[15px] items-center bg-[#EBEBEB] px-[134px] rounded-[17px] h-[58px] px-[30px] py-[18px] text-gray-500 text-[13px]"
        placeholder="어떤 여가를 더 원하시나요?">

      </textarea>

    </div>





  );
}
