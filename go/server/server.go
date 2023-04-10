package server

import (
	"entry_task/db"
	"entry_task/handler"
	"entry_task/repository"
	"entry_task/usecase"
	"entry_task/util"
	"net"
	"os"

	"github.com/joho/godotenv"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
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
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})

	dbErr := db.Connect()
	if dbErr != nil {
		log.Fatal().Msg("Error connecting to database")
	}

	server, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}
	log.Info().Msg("Server started on port 8080")

	authHandler := initServer()

	for {
		conn, err := server.Accept()
		if err != nil {
			log.Fatal().Msg("Failed to accept connection")
			panic("Failed to accept connection")
		}
		go authHandler.Handle(conn)
	}
}
