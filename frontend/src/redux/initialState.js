const initialState = {
	parameters: {
		title: "",
		difficulty: "1",
		description: ""
	},
	results: {
		title: "",
		task: "",
		files: [
			{ name: "przyklad.txt", content: "data:text/plain;base64,SGVsbG8gV29ybGQh" }, // Zawartość: "Hello World!"
			{ name: "test.cpp", content: "data:text/plain;base64,I2luY2x1ZGUgPGlvc3RyZWFtPgoKaW50IG1haW4oKSB7CiAgICBzdGQ6OmNvdXQgPDwgIkhlbGxvIFdvcmxkISIgPDwgc3RkOjplbmRsOwogICAgcmV0dXJuIDA7Cn0K" } // Prosty kod C++
		],
	},
};

export default initialState;