import { useRouter } from "next/router";


const GoogleCallback = () => {

  const router = useRouter()

  router.push("/")

  return;
};

export default GoogleCallback;