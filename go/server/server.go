package server

import (
	"entry_task/db"
	"entry_task/handler"
	"entry_task/repository"
	"entry_task/usecase"
	"entry_task/util"
	"fmt"
	"net"

	"github.com/joho/godotenv"
)

func initServer() *handler.AuthHandler {
	userRepo := repository.NewUserRepo(db.Get())
	authUtil := util.NewAuthUtil()

	authUsecase := usecase.NewAuthUsecase(&usecase.AuthUsecaseConfig{
		UserRepo: userRepo,
		AuthUtil: authUtil,
	})

	authHandler := handler.NewAuthHandler(authUsecase)

	return authHandler
}

func Init() {
	err := godotenv.Load(".env")
	if err != nil {
		panic(err)
	}

	dbErr := db.Connect()
	if dbErr != nil {
		fmt.Println("error connecting to DB")
	}

	server, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}
	fmt.Println("Server started on port 8080")

	authHandler := initServer()

	for {
		conn, err := server.Accept()
		if err != nil {
			panic(err)
		}
		go authHandler.Handle(conn)
	}
}
