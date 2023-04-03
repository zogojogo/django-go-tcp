package dto

type TCPRequestDTO struct {
	Action string      `json:"action"`
	Data   interface{} `json:"data"`
}

type TCPResponseDTO struct {
	Code    int         `json:"code"`
	Message string      `json:"message,omitempty"`
	Data    interface{} `json:"data,omitempty"`
}
