package handler

import (
	"encoding/json"
	"entry_task/domain"
	"entry_task/dto"
	"entry_task/usecase"
	"entry_task/util"
	"io"
	"net"
	"net/http"

	"github.com/rs/zerolog/log"
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
				log.Info().Msg("Connection closed")
				return
			}
			log.Fatal().Msg("Error reading request:" + err.Error())
			return
		}

		switch request.Action {
		case LOGIN_ACTION:
			h.handleLogin(request, encoder)
		case REGISTER_ACTION:
			h.handleRegister(request, encoder)
		default:
			if err := util.ResponseErrorJSON(http.StatusBadRequest, domain.ErrInvalidAction, encoder); err != nil {
				log.Fatal().Msg(domain.ErrInvalidAction.Error())
			}
			return
		}
	}
}

func (h *AuthHandler) handleRegister(data dto.TCPRequestDTO, encoder *json.Encoder) {
	var registerData dto.RegisterRequestDTO
	err := util.UnmarshalJSONData(data.Data, &registerData)
	if err != nil {
		if err = util.ResponseErrorJSON(http.StatusBadRequest, err, encoder); err != nil {
			log.Fatal().Msg("Error writing response:" + err.Error())
			return
		}
		return
	}

	authResp, err := h.authUsecase.Register(registerData)
	if err != nil {
		if err = util.ResponseErrorJSON(http.StatusBadRequest, err, encoder); err != nil {
			log.Fatal().Msg("Error writing response:" + err.Error())
			return
		}
		return
	}

	if err = util.ResponseSuccessJSON(http.StatusCreated, authResp, encoder); err != nil {
		log.Fatal().Msg("Error writing response:" + err.Error())
		return
	}
}

func (h *AuthHandler) handleLogin(data dto.TCPRequestDTO, encoder *json.Encoder) {
	var loginData dto.LoginRequestDTO
	err := util.UnmarshalJSONData(data.Data, &loginData)
	if err != nil {
		if err = util.ResponseErrorJSON(http.StatusBadRequest, err, encoder); err != nil {
			log.Fatal().Msg("Error writing response:" + err.Error())
			return
		}
		return
	}

	authResp, err := h.authUsecase.Login(loginData)
	if err != nil {
		if err_json := util.ResponseErrorJSON(http.StatusBadRequest, err, encoder); err_json != nil {
			log.Fatal().Msg("Error writing response:" + err_json.Error())
			return
		}
		return
	}

	if err_json := util.ResponseSuccessJSON(http.StatusOK, authResp, encoder); err_json != nil {
		log.Fatal().Msg("Error writing response:" + err_json.Error())
		return
	}
}
