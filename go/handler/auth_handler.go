package handler

import (
	"encoding/json"
	"entry_task/dto"
	"entry_task/usecase"
	"entry_task/util"
	"fmt"
	"io"
	"net"
	"net/http"
)

const (
	LOGIN_ACTION    string = "login"
	REGISTER_ACTION string = "register"
)

type AuthHandler struct {
	authUsecase usecase.AuthUsecase
}

func NewAuthHandler(authUsecase usecase.AuthUsecase) *AuthHandler {
	return &AuthHandler{authUsecase: authUsecase}
}

func (h *AuthHandler) Handle(conn net.Conn) {
	defer conn.Close()

	decoder := json.NewDecoder(conn)
	encoder := json.NewEncoder(conn)

	for {
		var request dto.TCPRequestDTO
		if err := decoder.Decode(&request); err != nil {
			if err == io.EOF {
				fmt.Println("Client closed connection:", err)
				return
			}
			fmt.Println("Error reading message:", err)
			return
		}

		switch request.Action {
		case LOGIN_ACTION:
			h.handleLogin(request, encoder)
		case REGISTER_ACTION:
			h.handleRegister(request, encoder)
		default:
			fmt.Println("Invalid action")
			return
		}
	}
}

func (h *AuthHandler) handleRegister(data dto.TCPRequestDTO, encoder *json.Encoder) {
	var registerData dto.RegisterRequestDTO
	print(data.Data)
	err := util.UnmarshalJSONData(data.Data, &registerData)
	if err != nil {
		if err = util.ResponseErrorJSON(http.StatusBadRequest, err, encoder); err != nil {
			fmt.Println("Error writing response:", err)
			return
		}
	}

	authResp, err := h.authUsecase.Register(registerData)
	if err != nil {
		if err = util.ResponseErrorJSON(http.StatusBadRequest, err, encoder); err != nil {
			fmt.Println("Error writing response:", err)
			return
		}
	}

	if err = util.ResponseSuccessJSON(authResp, encoder); err != nil {
		fmt.Println("Error writing response:", err)
		return
	}
}

func (h *AuthHandler) handleLogin(data dto.TCPRequestDTO, encoder *json.Encoder) {
	var loginData dto.LoginRequestDTO
	err := util.UnmarshalJSONData(data.Data, &loginData)
	if err != nil {
		if err = util.ResponseErrorJSON(http.StatusBadRequest, err, encoder); err != nil {
			fmt.Println("Error writing response:", err)
			return
		}
	}

	authResp, err := h.authUsecase.Login(loginData)
	if err != nil {
		if err = util.ResponseErrorJSON(http.StatusBadRequest, err, encoder); err != nil {
			fmt.Println("Error writing response:", err)
			return
		}
	}

	if err = util.ResponseSuccessJSON(authResp, encoder); err != nil {
		fmt.Println("Error writing response:", err)
		return
	}
}
