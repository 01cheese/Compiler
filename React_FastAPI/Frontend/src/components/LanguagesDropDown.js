import React, {useContext, useState} from "react";
import './MyDict.css'
import {languageOptions} from "../constants/languageOptions";


const LanguagesDropdown = ({onSelectChange, theme}) => {
    return (

        <div className={`languagesDropdownButton ${theme}`}>
            <div>
                {languageOptions.map((option, index) => (
                    <label key={option.value}>
                        <input
                            type="radio"
                            name="radio"
                            defaultChecked={index === 1}
                            onChange={() => onSelectChange(option)}
                        />
                        <span>{option.label}</span>
                    </label>
                ))}
            </div>
        </div>
    )
        ;
};

export default LanguagesDropdown;