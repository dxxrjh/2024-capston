import MypageSidebar from "@/components/MypageSidebar";


export default function Delete() {


  return (
    <div className="flex justify-center">

      <MypageSidebar />

      <div className="mt-[100px] flex flex-col justify-center items-center">
        <div className="grid grid-cols-[115px_auto] grid-rows-4 w-[590px] h-[272px] border rounded-[17px] shadow-custom">

          {/* 2x3 부분 */}
          <div className="border p-4 text-center">닉네임</div>
          <div className="border p-4 ">
            <textarea className="resize-none border h-[40px] text-[14px] rounded-8px"
              placeholder="value">
            </textarea>
          </div>
          <div className="border p-4 text-center">나이</div>
          <div className="border p-4 text-center">셀 4</div>
          <div className="border p-4 text-center">성별</div>
          <div className="border p-4 text-center">셀 6</div>

          {/* 병합된 한 줄 */}
          <div className="border p-4 text-center col-span-2">병합된 셀</div>
        </div>

        {/* <textarea className="resize-none border h-[40px] text-[14px] rounded-8px"
              placeholder="value">
            </textarea> */}



        <button className="rounded-[8px] w-[86px] h-[40px] bg-[#000000] text-white border mt-[30px] ">
          저장
        </button>
      </div>




    </div>



  );

}