import React from "react";
import { FaGithub, FaLinkedin } from "react-icons/fa";

const Footer = () => {
  return (
    <footer className="bg-primary bg-pattern py-4">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center gap-y-2 justify-center">
          <div className="flex gap-x-3 text-lg text-black">
            <a href="https://github.com/eraydmrcoglu">
              <FaGithub size={20} />
            </a>
            <a href="https://www.linkedin.com/in/eraydemircioglu/">
              <FaLinkedin size={20} />
            </a>
          </div>
          <div className="text-black font-medium text-sm">
            &copy; 2023. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
