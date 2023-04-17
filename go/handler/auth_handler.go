package handler

import (
	"entry_task/dto"
	"entry_task/pb"
	"entry_task/usecase"
	"entry_task/util"
	"fmt"
	"io"
	"net"
	"net/http"

	"github.com/rs/zerolog/log"
	"google.golang.org/protobuf/proto"
	"google.golang.org/protobuf/types/known/anypb"
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

	for {
		dataPb := pb.TCPRequest{}
		data := make([]byte, 4096)
		length, err := conn.Read(data)
		if err != nil {
			if err == io.EOF {
				log.Fatal().Msg("Client closed the connection")
				return
			}
			log.Fatal().Msg("Error reading request:" + err.Error())
			return
		}
		err = proto.Unmarshal(data[:length], &dataPb)
		if err != nil {
			fmt.Println(err.Error())
			err = util.WriteErrorTCPResponse(conn, http.StatusBadRequest, err.Error())
			if err != nil {
				fmt.Println(err.Error())
				return
			}
			return
		}

		switch dataPb.Action {
		case "test":
			h.handleTest(dataPb.Data, conn)
		}
	}
}

func (h *AuthHandler) handleTest(data *anypb.Any, conn net.Conn) {
	loginReq := &pb.LoginRequest{}
	if data.TypeUrl == "type.googleapis.com/LoginRequest" {
		err := proto.Unmarshal(data.Value, loginReq)
		if err != nil {
			fmt.Println(err.Error())
			err = util.WriteErrorTCPResponse(conn, http.StatusBadRequest, err.Error())
			if err != nil {
				fmt.Println(err.Error())
				return
			}
			return
		}
	}

	loginReqDTO := dto.LoginRequestDTO{
		Username: loginReq.Username,
		Password: loginReq.Password,
	}

	res, err := h.authUsecase.Login(loginReqDTO)
	if err != nil {
		fmt.Println(err.Error())
		err = util.WriteErrorTCPResponse(conn, http.StatusBadRequest, err.Error())
		if err != nil {
			fmt.Println(err.Error())
			return
		}
		return
	}

	response := &pb.AuthResponse{}
	response.AccessToken = res.Token

	authResponseBytes, err := proto.Marshal(response)
	if err != nil {
		fmt.Println(err.Error())
		err = util.WriteErrorTCPResponse(conn, http.StatusBadRequest, err.Error())
		if err != nil {
			fmt.Println(err.Error())
			return
		}
		return
	}

	authResponseAny, err := anypb.New(&anypb.Any{
		TypeUrl: "type.googleapis.com/AuthResponse",
		Value:   authResponseBytes,
	})
	if err != nil {
		fmt.Println(err.Error())
		err = util.WriteErrorTCPResponse(conn, http.StatusBadRequest, err.Error())
		if err != nil {
			fmt.Println(err.Error())
			return
		}
		return
	}

	err = util.WriteSuccessTCPResponse(conn, http.StatusOK, authResponseAny)
	if err != nil {
		fmt.Println(err)
		return
	}
}
