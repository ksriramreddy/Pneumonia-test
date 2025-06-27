import { useRef, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import './index.css'
import axios from 'axios'
import { Result } from 'postcss'
import noImage from "../public/noimage.png"

function App() {
  const [selectedImage, setSelectedImage ] = useState()
  const [result , setResult] = useState({"predicted" : null})
  const [isPrediction , setIsPredicting] = useState(false)
  const isFirstTime  = useRef(true)
  console.log(selectedImage);
  const BACKEND = import.meta.env.VITE_BACKEND_KEY;
  let width = "100"
  const predict =async ()=>{
    if(!selectedImage){
      alert("No Image Selected")
      return
    }

    setResult({"predicted" : null})
    if(isFirstTime.current){
      alert("If it is 1st Time. Please wait for some time with the server starts up...")
    }
    try {
      setIsPredicting(true)
      const formData = new FormData()
      formData.append("file",selectedImage)
      const resp = await axios.post(`${BACKEND}/predict`,formData,{
        headers : {"Content-Type" : "multipart/form-data"}
      })
      console.log(resp.data)  
      const result = resp.data
      console.log(result.predicted);
      if(result.message){
        alert(result.message)
        return
      }
      setResult(result)
      width = "100"
      setIsPredicting(false)
    } catch (error) {
      alert(error.message)
      console.log(error);
    }
  }
  
  return (
    <div className='flex flex-col gap-6 '>
      <div>
        <h1 className='font font-extrabold text-5xl'>👨‍⚕️PNEUMONIA DETECTION🩺</h1>
      </div>
    
    <div className='card bg-[#00ffa0] border-[4px] rounded-3xl border-[#05060f] border-solid flex md:flex-row flex-col gap-3 '>
      
      <div className='w-[50%] flex flex-col gap-2'>
        <img className='w-full border rounded-xl h-[200px] md:h-[500px]'  src={selectedImage? URL.createObjectURL(selectedImage) : noImage} alt="" />
        <input className='w-full p-2 bg-black rounded-lg  text-white ' onChange={(e)=>{setSelectedImage(e.target.files[0])
           setResult({"predicted" : null})}}  type="file" accept='image/*'/>
      </div>
      <div className='flex flex-col gap-3 justify-evenly '>
        
        <h1 className='text-left'> This model predicts whether a chest X-ray image shows signs of <span>PNEUMONIA</span> or is <span>NORMAL</span></h1>
        <h1 className='text-left'> This uses <span>ResNet-18</span> CNN and trained on around 5,800+ chest X-ray Images</h1>
        <h1 className=' w-full text-balance text-left'> To test Upload a  chest X-ray image(JPEG/PNG) get the prediction in real time</h1>
        <h1 className='text-left'>⚠️This tool is for <span>educational/demo</span>purposes and should not be used for medical diagnosis</h1>
        <h1 className='text-left'>🟩 NORMAL</h1>
        <h1 className='text-left'>🟥 PNEUMONIA</h1>
        <div  className='flex flex-col gap-3 w-[100%]' >
          <h1 className={`p-2 text-black rounded-lg font-bold bg-gradient-to-r bg-white ${result?.predicted == 0 ? "from-green-500 to-green-500 bg-[length:100%_100%]":result?.predicted == null? "from-red-500 to-red-500 bg-[length:0%_100%]" : "from-red-500 to-red-500 bg-[length:100%_100%]"} transition-all duration-700 ease-in-out bg-no-repeat`}>NORMAL</h1>
          <h1  className={`p-2 text-black rounded-lg font-bold bg-white bg-gradient-to-r  ${result?.predicted == 1 ? "from-green-500 to-green-500 bg-[length:100%_100%]":result?.predicted == null? "from-red-500 to-red-500 bg-[length:0%_100%]" : "from-red-500 to-red-500 bg-[length:100%_100%]"} transition-all duration-700 ease-in-out bg-no-repeat`
          }>PNEUMONIA</h1>
        </div>
        <button onClick={predict} className='p-2 bg-green-600 bg-opacity-75 border-[2px]  border-gray-600  rounded-lg font-semibold text-xl'>{
          isPrediction? "Prediction..." : "Predict"
        }</button>
      </div>
    </div>
    </div>
  )
}

export default App

// function noImage(){
//   return(
//     <div className='w-full h-full flex items-center justify-center bg-gray-400 text-opacity-60'>
//       NO IMAGE SELECTED
//     </div>
//   )
// }