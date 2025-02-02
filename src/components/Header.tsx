import Image from "next/image";
import Router from "next/router";

const Header = () => {
  const logoButtonClick = () => {
    Router.push("/main")
  }

  return (
    <button className="flex mt-[40px] items-center justify-center"
      onClick={logoButtonClick} >
      <Image src="/images/logo_forrest.png" alt="logo" width={50} height={50} >
      </Image>
      <h1 className="text-green-900 text-[32px] font-bold">
        For-rest
      </h1>
    </button>
  );

}

export default Header;