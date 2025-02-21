const buttonColor = "#FFF";
const buttonHover = "#e7e7e7";
const primaryColor = "#008000FF";
const fontColor = '#000';
const borderRadius = "10px";

export const customStyles = {
    control: (styles) => ({
        ...styles,
        width: "100%",
        maxWidth: "14rem",
        minWidth: "12rem",
        borderRadius: borderRadius,
        color: fontColor,
        fontSize: "0.8rem",
        lineHeight: "1.75rem",
        backgroundColor: buttonColor,
        cursor: "pointer",
        outline: "none",
        ":hover": {
            border: "1.5px solid #4169e1"
        },
    }),
    option: (styles) => {
        return {
            ...styles,
            color: "#000",
            fontSize: "0.8rem",
            lineHeight: "1.75rem",
            width: "100%",
            background: "#fff",
            transition: "all 0.1s ease-in-out",
            ":hover": {
                backgroundColor: primaryColor,
                color: "#fff",
                cursor: "pointer",
            },
        };
    },
    menu: (styles) => {
        return {
            ...styles,
            backgroundColor: "#fff",
            maxWidth: "14rem",
            border: "1px solid #000000",
            borderRadius: borderRadius

        };
    },

    placeholder: (defaultStyles) => {
        return {
            ...defaultStyles,
            color: fontColor,
            fontSize: "0.8rem",
            lineHeight: "1.75rem",
        };
    },

};