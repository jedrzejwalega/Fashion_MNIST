import input_data
import train_test
import fmnist_dataset
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



def main():
    args = input_data.get_user_input()
    fmnist_dataset.download_mnist(args.path)
    train_images, train_labels = fmnist_dataset.load_mnist(args.path)
    test_images, test_labels = fmnist_dataset.load_mnist(args.path, kind="test")
    program = train_test.RunManager(learning_rates=args.learning_rates, 
                                    epochs=args.epochs,
                                    shuffle=args.shuffle, 
                                    find_lr=args.find_lr, 
                                    batch_size=args.batch_size,
                                    gamma=args.gamma,
                                    gamma_step=args.gamma_step,
                                    architectures=args.architecture)
    program.pass_datasets((train_images, train_labels), (test_images, test_labels))
    program.train()
    if args.test:
        program.test()
    if args.write_model:
        program.write_best_model(args.write_model)

if __name__ == "__main__":
    main()