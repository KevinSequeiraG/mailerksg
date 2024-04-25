/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html", "./templates/mails/*.html"],
  theme: {
    screens: {
      mdx250: "250px",
      mdx300: "300px",
      mdx350: "350px",
      mdx400: "400px",
      mdx450: "450px",
      mdx500: "500px",
      mdx550: "550px",
      mdx600: "600px",
      mdx650: "650px",
      mdx700: "700px",
      mdx750: "750px",
      mdx800: "800px",
      mdx850: "850px",
      mdx900: "900px",
      mdx950: "950px",
      mdx1000: "1000px",
      mdx1050: "1050px",
      mdx1100: "1100px",
      mdx1150: "1150px",
      mdx1200: "1200px",
      mdx1250: "1250px",
      mdx1300: "1300px",
      mdx1350: "1350px",
      mdx1400: "1400px",
      mdx1450: "1450px",
      mdx1500: "1500px",
      mdx1550: "1550px",
      mdx1600: "1600px",
      mdx1650: "1650px",
      mdx1700: "1700px",
      mdx1750: "1750px",
      mdx1800: "1800px",
      mdx1850: "1850px",
      mdx1900: "1900px",
      mdx1950: "1950px",
      mdx2000: "2000px"
    },
    fontFamily: {
      'rubik': ['Rubik', 'sans-serif'],
      'rufina': ['Rufina', 'sans-serif'],
      'raleway': ['Raleway', 'sans-serif']
    },
    extend: {
      boxShadow: {
        'searchbar': '0px 1px 5px #dddddd',
        'mail': '0px 1px 5px #dddddd'
      }
    },
  },
  plugins: [],
}



