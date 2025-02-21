import React from 'react'
import { classnames } from '../utils/general'


const CustomInput = ({ customInput, setCustomInput }) => {
    return (
        <>
            {" "}
            <textarea

                rows="5"
                value={customInput}
                onChange={(e) => setCustomInput(e.target.value)}
                placeholder="Custom Input"
            ></textarea>
        </>
    )
}

export default CustomInput;