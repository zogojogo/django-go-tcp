package dto

type JwtResponse struct {
	UserId   int64  `json:"user_id"`
	Username string `json:"username"`
}

type LoginRequestDTO struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type RegisterRequestDTO struct {
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

type AuthResponseDTO struct {
	Token string `json:"access_token"`
}

type TCPRequestDTO struct {
	Action string      `json:"action"`
	Data   interface{} `json:"data"`
}
