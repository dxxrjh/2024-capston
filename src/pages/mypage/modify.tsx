import MypageSidebar from "@/components/MypageSidebar";


export default function Modify() {


  return (
    <div className="flex justify-center">

      <MypageSidebar />
      <div className="mt-[100px] flex flex-col justify-center items-center">
        <div className="grid grid-cols-[115px_auto] grid-rows-4 w-[590px] h-[272px] border rounded-[17px] shadow-custom">

          {/* 2x3 부분 */}
          <div className="text-[#9A9A9A] border p-4 text-center">닉네임</div>

          <div className="border p-4">
            <textarea className="resize-none border h-[40px] text-[14px] rounded-8px"
              placeholder="value">
            </textarea>
          </div>

          <div className="text-[#9A9A9A] border p-4 text-center">나이</div>

          <div className="border p-4 text-center">
            <select className="border rounded px-2 py-1 w-full max-h-32 overflow-auto">
              {Array.from({ length: 41 }, (_, i) => 15 + i).map((age) => (
                <option key={age} value={age}>{age}</option>
              ))}
            </select>
          </div>


          <div className="text-[#9A9A9A] border p-4 text-center">성별</div>


          <div className="border p-4 text-center flex flex-row gap-4">
            <label className="flex items-center space-x-2">
              <input type="radio" name="gender" value="male" className="w-5 h-5 text-blue-600 border-gray-300 focus:ring-blue-500" />
              <span>남성</span>
            </label>
            <label className="flex items-center space-x-2">
              <input type="radio" name="gender" value="female" className="w-5 h-5 text-blue-600 border-gray-300 focus:ring-blue-500" />
              <span>여성</span>
            </label>
            <label className="flex items-center space-x-2">
              <input type="radio" name="gender" value="other" className="w-5 h-5 text-blue-600 border-gray-300 focus:ring-blue-500" />
              <span>기타</span>
            </label>
          </div>




          {/* 병합된 한 줄 - col-span-2 */}
          <div className="border p-4 col-span-2 flex items-center space-x-2">
            <input type="checkbox" className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
            <span className="text-[#9A9A9A]">위치 정보 제공에 동의합니다.</span>
          </div>



        </div>

        <button className="rounded-[8px] w-[86px] h-[40px] bg-[#000000] text-white border mt-[30px] ">
          저장
        </button>



      </div>
    </div >
  );

}